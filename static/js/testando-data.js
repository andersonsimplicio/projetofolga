
// txtData - é a data inicial.
// DiasAdd - É quantos dias você quer adicionar a txtData.
function SomarData() {
		var txtData = "28/09/2019"; //poder ser qualquer outra
		var DiasAdd = 3 // Aqui vem quantos dias você quer adicionar a data
		var d = new Date();
			// depois, em milisegundos, eu multiplico um dia (86400000 milisegundos)
        var data_hoje = d.toLocaleDateString("pt-br",{day: '2-digit'});
        var teste = new Date();
        teste.setDate(d.getDate() + DiasAdd);
        console.log(teste.toLocaleDateString("pt-br",{day: '2-digit'}));












		// Crio a var da DataFinal			
		var DataFinal;
		// Aqui comparo o dia no objeto d.getDate() e vejo se é menor que dia 10.			
		if(d.getDate() < 10){
			// Se o dia for menor que 10 eu coloca o zero no inicio
			// e depois transformo em string com o toString()
			// para o zero ser reconhecido como uma string e não
			// como um número.
			DataFinal = "0"+d.getDate().toString();
		}else{	
			// Aqui a mesma coisa, porém se a data for maior do que 10 não tenho necessidade de colocar um zero na frente.
			DataFinal = d.getDate().toString();	
		}
		// Aqui, já com a soma do mês, vejo se é menor do que 10 se for coloco o zero ou não.
		if((d.getMonth()+1) < 10){
			DataFinal += "0"+(d.getMonth()+1).toString();
		}
		else
		{
			DataFinal += (d.getMonth()+1).toString()+"/"+d.getFullYear().toString();
		}
	//console.log(DataFinal);
}