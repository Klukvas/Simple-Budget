
document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.querySelector('#id_category');
    const subcategorySelect = document.querySelector('#id_subcategory');

    categorySelect.addEventListener('change', function() {
        const categoryId = this.value;

        fetch(`/simple-budget/get-subcategories/${categoryId}/`)
            .then(response => response.json())
            .then(data => {
                subcategorySelect.innerHTML = '<option value="">---------</option>';
                data.subcategories.forEach(subcategory => {
                    const option = document.createElement('option');
                    option.value = subcategory.id;
                    option.textContent = subcategory.name;
                    subcategorySelect.appendChild(option);
                });
            });
    });
});
