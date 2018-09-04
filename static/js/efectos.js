(function(){
    var menuLateral = document.getElementById('open-hide');
    var btnMenu = document.getElementById("open-hide-btn");
    var btnMenuQuery = document.getElementById("open-hide-btn-query");
    btnMenu.addEventListener('click', ()=>{
        menuLateral.classList.toggle('show-menu');
    btnMenuQuery.addEventListener('click', ()=>{
        menuLateral.classList.toggle('query-sidebar');
    });
});


})();

