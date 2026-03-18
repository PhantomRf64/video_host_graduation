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

const input = document.getElementById('tagsInput');
const wrapper = document.getElementById('tagsWrapper');
const hidden = document.getElementById('tagsHidden');

let tags = [];

function updateHidden() {
    hidden.value = tags.join(', ');
}

function createTag(text) {
    if (tags.includes(text)) return;

    tags.push(text);
    updateHidden();

    const tag = document.createElement('div');
    tag.classList.add('tag-chip');

    tag.innerHTML = `${text} <span>&times;</span>`;

    tag.querySelector('span').onclick = () => {
        tags = tags.filter(t => t !== text);
        tag.remove();
        updateHidden();
    };

    wrapper.insertBefore(tag, input);
}

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ',') {
        e.preventDefault();

        const value = input.value.trim();
        if (value) {
            createTag(value);
            input.value = '';
        }
    }
});

wrapper.addEventListener('click', () => input.focus());