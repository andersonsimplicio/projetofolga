// $(function() {
//     $( "#date1" ).datepicker({
//         showButtonPanel:true,
//         changeMonth: true,
//         changeYear: true,
//         showOtherMonths: true,
//         selectOtherMonths: false,
//         numberOfMonths: 2,
//         dateFormat: 'dd/mm/yy',
//         dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'],
//         dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
//         dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
//         monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
//         monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
//     });
    
// });

$(function() {
    $( "#date1" ).datepicker({
        showButtonPanel:true,
        selectOtherMonths: false,
        dateFormat: 'dd/mm/yy',
        dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'],
        dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
        dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
        monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
        monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
    });
    
    $("#date2").datepicker({
        showButtonPanel:true,
        selectOtherMonths: false,
        dateFormat: 'dd/mm/yy',
        dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'],
        dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
        dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
        monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
        monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
    });
    
});

    var d = new Date();
    var mes = d.getMonth();
    console.log("esse é o mes" +mes);
    $("#mes").text(mes);


    $("#date1").on(function(){
        
        var begin = new Date();
        var begin1 = $("#date1").val().split("/",1)[0];
        console.log(begin1);
        begin.setDate(begin1);
        console.log(begin);
        var dia  = begin.getDate();
        console.log(dia);

    
     $("#date2").focusout(function(){
        //var end = $("#date2").val().split("/",1)[0];
        var end = new Date();
        end.setDate($("#date2").val().split("/",1)[0]);
        console.log(end);
//     var table = '';
//     while (begin <= end){
//         table += '<td>' + begin + '</td>';
//         begin++;
        
//     }
//     $(".days_of_month").html(table);
    
  

 });
});