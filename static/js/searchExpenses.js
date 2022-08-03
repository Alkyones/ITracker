const searchBar = document.querySelector('#searchBar');
const outputTable = document.querySelector('.table-output');
const allexpensesTable = document.querySelector('.all-expenses-table');
const paginationContainer = document.querySelector('.pagination-container');
const tableBody = document.querySelector('.table-body');
outputTable.style.display = 'none';

searchBar.addEventListener('keyup', (e)=> {
    const searchTValue = e.target.value;
    
    if (searchTValue.trim().length > 0){
        paginationContainer.style.display = 'none'; //
        tableBody.innerHTML = '';
        fetch("/search-expense/",{
        body:JSON.stringify({search_text: searchTValue}),
        method: 'POST'
        })
        .then((res) => res.json())
        .then((data)=> {console.log(data);
            allexpensesTable.style.display = 'none';
            outputTable.style.display = 'block';
            if(data.length===0){
                outputTable.innerHTML = 'No results founds';
            }else{
                data.forEach(item=>{
                tableBody.innerHTML += `
                <tr>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td><a href="{% url 'edit-expense' ${item.id}" class="btn btn-sm btn-outline-info">Edit</a>
                        <a href="{% url 'delete-expense' ${item.id}" class="btn btn-sm btn-outline-danger">Delete</a></td>
                </tr>`; 
            })
        }
    })}else {
        allexpensesTable.style.display = 'block';
        paginationContainer.style.display = 'block';
        outputTable.style.display = 'none';
    }
})