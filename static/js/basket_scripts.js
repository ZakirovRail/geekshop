window.onload = function () {
    /*
    // можем получить DOM-объект меню через JS
    var menu = document.getElementsByClassName('menu')[0];
    menu.addEventListener('click', function () {
        console.log(event);
        event.preventDefault();
    });
    
    // можем получить DOM-объект меню через jQuery
    $('.menu').on('click', 'a', function () {
        console.log('event', event);
        console.log('this', this);
        console.log('event.target', event.target);
        event.preventDefault();
    });
   
    // получаем атрибут href
    $('.menu').on('click', 'a', function () {
        var target_href = event.target.href;
        if (target_href) {
            console.log('нужно перейти: ', target_href);
        }
        event.preventDefault();
    });
    */

    // добавляем ajax-обработчик для обновления количества товара
    $('.basket_list').on('click', 'input[type="number"]', function () {
        let target_href = event.target;

        if (target_href) {
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",

                success: function (data) {
                    $('.basket_list').html(data.result);
                    console.log('ajax done');
                },
            });
        }
        event.preventDefault();
        // return;
    });

    $('.basket_list').on('click', '.button-remove', function (){
        let pk = $(this).attr('data-pk');
        if(pk){
            $.ajax({
                url: "/basket/remove/ajax" + pk + "/",

                success: function (data){
                    $('.basket_list').html(data.result);
                    console.log('this delete function works once only. It is a bug');
                }
            });
        }
        return;
    });

};

/*
    // Пример дефекта для кнопки "УДАЛИТЬ" в корзине, когда кнопка отрабатывает только 1 раз. Чтбы сработало второй
    // раз, то надо обновлять страницу

 */
//     $('.button-remove').on(types: 'click', selector: function(){
//         let pk = $(this).attr(name:'data-pk');
//         if(pk){
//             $.ajax(url:{
//                 url: "/basket/remove/ajax" + pk + "/",
//
//                 success: function (data) {
//                     $('.basket_list').html(data.result);
//                 }
//             });
//         }
//         return;
//     });
//
// };

//     $('.button-remove').on('click', function (){
//         let pk = $(this).attr('data-pk');
//         if(pk){
//             $.ajax({
//                 url: "/basket/remove/ajax" + pk + "/",
//
//                 success: function (data) {
//                     $('.basket_list').html(data.result);
//                     console.log('this delete function works once only. It is a bug');
//                 }
//             });
//         }
//         return;
//     });
//
// };