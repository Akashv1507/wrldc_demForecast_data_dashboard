//custom validation before form submit
function validateForm() {
    // checking if any file is uploaded
    if( document.getElementById("excleFile").files.length == 0 ){
        errorDiv.innerHTML = "<b> Error !!!! Please select any csv/excel file  ";
        return false;
    }
    
    //true will submit form ,false will not
    return true;
}

//styling inout file
const file = document.querySelector('#excleFile');
file.addEventListener('change', (e) => {
  // Get the selected file
  const [file] = e.target.files;
  // Get the file name and size
  const { name: fileName, size } = file;
  // Convert size in bytes to kilo bytes
  const fileSize = (size / 1000).toFixed(2);
  // Set the text content
  const fileNameAndSize = `${fileName} - ${fileSize}KB`;
  document.querySelector('.file-name').textContent = fileNameAndSize;
});