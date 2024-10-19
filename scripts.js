// file upload interface 
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');

// function to prevent default browser behavior 
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropegation();
}

dropArea.addEventListener('dragover', preventDefaults);
dropArea.addEventListener('dragenter', preventDefaults);
dropArea.addEventListener('dragleave', preventDefaults);

dropArea.addEventListener('drop', handleDrop);

dropArea.addEventListener('dragover', () => {
    dropArea.classList.add('drag-over');
  });
  
  dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('drag-over');
  });

