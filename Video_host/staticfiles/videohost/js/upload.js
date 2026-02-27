document.addEventListener("DOMContentLoaded", function () {

    const videoInput = document.getElementById("videoInput");
    const previewInput = document.getElementById("previewInput");

    if (videoInput) {
        videoInput.addEventListener("change", function () {
            const fileName = this.files.length ? this.files[0].name : "";
            document.getElementById("videoFileName").textContent = fileName;
        });
    }

    if (previewInput) {
        previewInput.addEventListener("change", function () {
            const fileName = this.files.length ? this.files[0].name : "";
            document.getElementById("previewFileName").textContent = fileName;
        });
    }

});