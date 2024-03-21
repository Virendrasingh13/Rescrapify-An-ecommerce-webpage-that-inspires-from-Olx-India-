document.getElementById('image').addEventListener('change', function(event) {
    var input = event.target;
    var reader = new FileReader();
    const imagePreview = document.getElementById('image-preview');
    const imagespan = document.getElementById('imagespan');
    
    const file = input.files[0];
    if(file){
        reader.onload = function() {
            var dataURL = reader.result;
            
            imagePreview.src = dataURL;
            imagePreview.style.display = 'block'
            imagePreview.style.position = 'relative'
            imagespan.style.visibility = 'hidden'
        };
        
        reader.readAsDataURL(input.files[0]);
    }
    else{
        
        if(typeof user_image_url !== 'undefined'){
            if (user_image_url) {
                imagePreview.src = user_image_url;
            }
        }else {
                imagePreview.style.display = 'none';
                imagespan.style.visibility = 'visible';
        }
        
        
    }
});

