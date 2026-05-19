import pynetbox
import platform
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- KONFIGURASI ---
TELEGRAM_TOKEN = 'TOKEN'
NB_URL = 'NETBOX_URL'
NB_TOKEN = 'TOKEN'

nb = pynetbox.api(url=NB_URL, token=NB_TOKEN)
NAMA_ANDA = "NAMA_ANDA"

# ================== UPDATE NETBOX ==================
def update_netbox_device(device):
    try:
        # 1. Update status
        device.status = "offline"

        # 2. Tambahkan deskripsi
        note = f"Audited by {NAMA_ANDA}"

        # Jika sudah ada deskripsi sebelumnya
        if device.description:
            if note not in device.description:
                device.description += f" | {note}"
        else:
            device.description = note

        # 3. Simpan perubahan
        device.save()

        return True

    except Exception as e:
        print("Error update Netbox:", e)
        return False

async def cek_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Format salah! Gunakan: /cek [Nama-Router]")
        return

    device_name = context.args[0]
    await update.message.reply_text(f"🔍 Mencari data {device_name} di Netbox...")

    try:
        device = nb.dcim.devices.get(name=device_name)
        if not device or not device.primary_ip:
            await update.message.reply_text(f"❌ Device '{device_name}' tidak ditemukan.")
            return

        target_ip = str(device.primary_ip.address).split('/')[0]
        await update.message.reply_text(f"📡 Mencoba PING ke {target_ip}...")

        is_windows = platform.system().lower() == 'windows'
        param = '-n' if is_windows else '-c'
        
        try:
            output = subprocess.check_output(
                ['ping', param, '1', target_ip],
                stderr=subprocess.STDOUT, universal_newlines=True, shell=is_windows
            )
            is_online = "TTL=" in output.upper()
        except:
            is_online = False

        status_msg = f"✅ {device_name} is ONLINE" if is_online else f"🔴 {device_name} is OFFLINE"
        await update.message.reply_text(status_msg)

        if not is_online:
            success = update_netbox_device(device)

            if success:
                await update.message.reply_text(
                    f"  *Netbox Updated!*\n"
                    f"• Status: Offline\n"
                    f"• Description: Audited by {NAMA_ANDA}\n\n"
                    f"  Device *{device_name}* mati → database berhasil diperbarui.",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "  Gagal update ke Netbox."
                )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("cek", cek_status))
    print("Bot is polling...")
    app.run_polling()
