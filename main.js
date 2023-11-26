function addSupplier(){
    pywebview.api.addSupplier('data');
}
function cancelAddSupplier(){
    pywebview.api.cancelAddSupplier('data');
}
function populateSuppliers(data){
    data = JSON.parse(atob(data).toString());
    document.getElementById('sup-sel').innerHTML="";
    for(var i=0; i<data.length; i++){
        document.getElementById('sup-sel').innerHTML+="<option id='S"+data[i]['id']+"'>"+data[i]['name']+"</option>";
    }
}