(function(){
    var menuLateral = document.getElementById('open-hide');
    // menuLateral.addEventListener('mouseenter', ()=>{
    //     menuLateral.classList.remove('show');
    // });

    // menuLateral.addEventListener('mouseleave', ()=>{
    //     menuLateral.classList.add('show');
    // });

    var btnMenu = document.getElementById("open-hide-btn");
    btnMenu.addEventListener('click', ()=>{
        menuLateral.classList.toggle('show-menu');
});
})();

