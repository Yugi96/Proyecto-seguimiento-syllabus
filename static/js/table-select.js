function selectedRow(){ 
    var index;
    var table = document.getElementById("table");
    document.getElementById("cedula").textContent = table.rows[1].cells[0].innerHTML;
    document.getElementById("nombres").textContent = table.rows[1].cells[1].innerHTML;
    document.getElementById("apellidos").textContent = table.rows[1].cells[2].innerHTML;
    document.getElementById("telefono").textContent = table.rows[1].cells[3].innerHTML;
    document.getElementById("correo").textContent = table.rows[1].cells[4].innerHTML;
    for(var i = 1; i < table.rows.length; i++){
        table.rows[i].onclick = function(){
            document.getElementById("cedula").textContent = this.cells[0].innerHTML;
            document.getElementById("nombres").textContent = this.cells[1].innerHTML;
            document.getElementById("apellidos").textContent = this.cells[2].innerHTML;
            document.getElementById("telefono").textContent = this.cells[3].innerHTML;
            document.getElementById("correo").textContent = this.cells[4].innerHTML;
            if(typeof index !== "undefined"){
               table.rows[index].classList.toggle("hover-row");
            }
            // get the selected row index
            index = this.rowIndex;
            // add class selected to the row
            this.classList.toggle("hover-row");
         };
    }
}
selectedRow();