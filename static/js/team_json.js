window.onload = function(){
    console.log("entrou");

$.getJSON("json/funcionarios.json", function(data) {
    let funcionarios = data.funcionarios;
    let saida = '';
    for (i = 0; i < funcionarios.length; i++) {
      saida += '<th class="bg-success">';
      //saida += '<td">' + funcionarios[i].equipe + '</td>';
      saida += '<td>' + funcionarios[i].nome + '</td>';
      saida += '</th>';
    }
  
    $("#cor_table").html(saida);
    console.log(saida);
  });

}