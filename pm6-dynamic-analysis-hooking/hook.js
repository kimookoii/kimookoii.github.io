Java.perform(function () {
    try {
        var CM = Java.use("com.example.app.utils.CredentialManager");
        CM.getApiKey.implementation = function () {
            var key = this.getApiKey();
            console.log("[HOOK] getApiKey -> " + key);
            return key;
        };
    } catch (e) {
        console.log("[ERROR] " + e);
    }
});