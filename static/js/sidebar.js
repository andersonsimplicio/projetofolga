
    

$(document).ready(function () {
        $(".sidebar").mCustomScrollbar({
        theme: "minimal"
    });
        

        if ($(window).width() <= 977) {
            $('.sidebar').addClass('disabled');
            $('#content').addClass('active');
        }else{
           $('.sidebar').removeClass('disabled');
           $('#content').removeClass('active');
        }


});

    $('.side-collapse').on('click', function () {
        if ($(window).width() <= 977) {
            $('.sidebar').toggleClass('disabled');
        }else{
            $('.sidebar').toggleClass('disabled');
            $('#content').toggleClass('active');   
        }
         

    });


    


$(window).resize(function () {
        if ($(window).width() <= 977) {
            $('.sidebar').addClass('disabled');
            $('#content').addClass('active');
        }else{
           $('.sidebar').removeClass('disabled');
           $('#content').removeClass('active');
        }


});


