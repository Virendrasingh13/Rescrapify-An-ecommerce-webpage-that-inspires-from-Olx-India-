const selectType = document.getElementById('selectType');
const selectCategory = document.getElementById('selectCategory');
console.log(selectCategory)
console.log(selectType)
selectType.addEventListener('change', function (){
    selectCategory.innerHTML = '<option selected disabled value="">Choose Category</option>'

    var selectedType = selectType.value;
    fetch(get_categories_by_type+"?type="+selectedType)
    .then(response => response.json())
    .then(data => {
        if (data.success){
            data.categories.forEach(category => {
                var option = document.createElement('option');
                option.text = category.category_name.toUpperCase();
                option.value = category.slug;
                selectCategory.appendChild(option);
            });

            selectCategory.disabled = data.length === 0;
        }
        else{
            alert(data.message)
        }
        
    })
    .catch(error =>{
        alert(error)
    });
});
