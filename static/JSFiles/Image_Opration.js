const img_data = document.getElementById('upload-form-img');
const loading2 = document.getElementById('loading2');

function getResizedFileName(picPath) {
    // Get just the filename, remove any query strings
    let dotIndex = picPath.lastIndexOf('.');
    let baseName = dotIndex !== -1 ? picPath.substring(0, dotIndex) : picPath;
    return baseName + "_resized.jpg";
}

img_data.addEventListener("submit", async(e) => {
    e.preventDefault();

    const formData = new FormData(img_data);
    loading2.style.display = 'block'; // Show loading

    //Debug What beeing sent
    const data = {}
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    console.log("Returned: ",data)

    try {
        const response = await fetch('http://127.0.0.1:8000/edit_image/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            console.log(blob)
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = getResizedFileName(data.imag_file.name); // use correct filename
            a.textContent = 'Download Image'
            document.getElementById('response_img').appendChild(a);
        }).catch(error => console.error('Error:', error));
        loading2.style.display = 'none'; // Hide loading
        
    } catch (error) {

        console.error(error);
        document.getElementById('response_img').innerHTML = `Error uploading file`;
        
    }
})