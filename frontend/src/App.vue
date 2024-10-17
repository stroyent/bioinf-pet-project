<template>
    <form name="file-upload" id="file-upload-form" action="http://localhost:8000/file/upload-csv" method="post" enctype="multipart/form-data" @submit.prevent="uploadFile">
        <label for="file">Upload CSV</label>
        <input id="file" name="file" type="file" accept=".csv" />
        <button>Upload</button>
    </form>
    <a href="http://localhost:8000/file/download" download v-show="linkReady">Download CSV</a>
    
</template>

<script setup>
import { onMounted, ref } from 'vue';
let fileUploadForm,
    linkReady = ref(false);

onMounted(() => {
    fileUploadForm = document.getElementById('file-upload-form');
})

function uploadFile() {
    fetch("http://localhost:8000/file/upload-csv",{
        method: 'POST',
        body: new FormData(fileUploadForm),
    })
    .then(response => response.json())
    .then((result) => {
        console.log('Success:', result);
        if (result.filename) {
            linkReady.value = true;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

</script>

<style>
.mainContainer {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
}

</style>
