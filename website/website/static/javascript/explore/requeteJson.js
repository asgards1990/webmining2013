
$(document).ready(function(){
//envoiDeLaRequete()
//alert("hello")
setTimeout(function(){envoiDeLaRequeteSearch()},1000)
//$("#title").click(function(){envoiDeLaRequeteSearch()})
//$("#title").click(function(){envoiDeLaRequetePredict()})
})

function genererRequetePredict(){
	var requestInter=new Object();
	requestInter.actors=new Array();
	for(var i=0;i<document.getElementById("actorsdesc").getElementsByClassName("actor").length;i++){
		requestInter.actors[i]=document.getElementById("actorsdesc").getElementsByClassName("actor")[i].id;
	}
	requestInter.genres=new Array();
	for(var i=0;i<document.getElementById("genre").getElementsByClassName("genre").length;i++){
		requestInter.genres[i]=document.getElementById("genre").getElementsByClassName("genre")[i].value;
	}
	requestInter.keywords=new Array();
	for(var i=0;i<document.getElementById("keywordsdesc").getElementsByClassName("name").length;i++){
		requestInter.keywords[i]=document.getElementById("keywordsdesc").getElementsByClassName("name")[i].textContent;
	}
	requestInter.directors=new Array();
	for(var i=0;i<document.getElementById("directors").getElementsByClassName("director").length;i++){
		requestInter.directors[i]=document.getElementById("directors").getElementsByClassName("director")[i].id;
	}
	//requestInter.budget=10.2;
	//
	//requestInter.release_period=new Object();
	//requestInter.release_period.season="summer";
	//requestInter.language="fr";
	
	return requestInter;
}

function envoiDeLaRequetePredict(){
	alert(JSON.stringify(genererRequetePredict()))
	$.post("http://senellart.com:8080/predict/","json_request="+JSON.stringify(genererRequetePredict()),fctCallbackPredict,"json")
}

function fctCallbackPredict(data){
	alert(JSON.stringify(data))
	//arreter=true;document.getElementById("loaderProvisoire").parentNode.removeChild(document.getElementById("loaderProvisoire"));montrerResultats("cadreProches");carrousel("cadreCoverflow");
}


function genererRequeteSearch(){
	var requestInter=new Object();
	requestInter.id=document.getElementById("moviesearch").children[0].id;
	requestInter.nbresults=10;
	requestInter.criteria=new Object();
	requestInter.criteria.actor_director=$("#acteurs").prop("checked");
	requestInter.criteria.genre=$("#genre").prop("checked");
	requestInter.criteria.budget=$("#budgets").prop("checked");
	requestInter.criteria.review=$("#review").prop("checked");
	/*requestInter.filter=new Object();
	requestInter.filter.actors=new Array();
	var compteur=0;
	for(var i=0;i<document.getElementById("actors").getElementsByClassName("actor").length;i++){
		if (document.getElementById("actors").getElementsByClassName("actor")[i].children[0].checked==true){
			requestInter.filter.actors[compteur]=document.getElementById("actors").getElementsByClassName("actor")[i].children[1].id;
			compteur=compteur+1;
		}
	}
	requestInter.filter.directors=new Array();
	compteur=0;
	for(var i=0;i<document.getElementById("actors").getElementsByClassName("director").length;i++){
		if (document.getElementById("actors").getElementsByClassName("director")[i].children[0].checked==true){
			requestInter.filter.directors[compteur]=document.getElementById("actors").getElementsByClassName("director")[i].children[1].id;
			compteur=compteur+1;
		}
	}
	requestInter.filter.genres=new Array();
	compteur=0;
	for(var i=0;i<document.getElementById("genres").getElementsByClassName("genre").length;i++){
		if (document.getElementById("genres").getElementsByClassName("genre")[i].children[0].checked==true){
			requestInter.filter.genres[compteur]=document.getElementById("genres").getElementsByClassName("genre")[i].children[1].textContent;
			compteur=compteur+1;
		}
	}
	requestInter.filter.budget=new Object();
	requestInter.filter.budget.min=budgetMin;
	requestInter.filter.budget.max=budgetMax;
	requestInter.filter.reviews=new Object();
	requestInter.filter.reviews.min=valueStar;
	/*requestInter.filter.release_period=new Object();
	requestInter.filter.release_period.begin="1900-01-01"; //inutile
	requestInter.filter.release_period.end="2100-01-01"; //inutile*/
	return requestInter;
}

function envoiDeLaRequeteSearch(){
	//alert("hello")
	alert(JSON.stringify(genererRequeteSearch()))
	//$.post("http://senellart.com:8080/search/","json_request="+JSON.stringify(genererRequeteSearch()),fctCallbackSearch,"json")
	var data=new Object;
	data.success=true;
	data.nbresults=4;
	data.results=new Array;
	data.results[0]=new Object;
	data.results[0].id="tt1951264";
	data.results[0].title="Hunger Games: L'embrasement";
	data.results[0].value=0.25;
	data.results[1]=new Object;
	data.results[1].id="tt2294629";
	data.results[1].title="La reine des neiges";
	data.results[1].value=0.8;
	data.results[2]=new Object;
	data.results[2].id="tt1981115";
	data.results[2].title="Thor: Le Monde des Ténèbres";
	data.results[2].value=0.5;
	data.results[3]=new Object;
	data.results[3].id="tt0816442";
	data.results[3].title="La Voleuse de livres";
	data.results[3].value=0;
	fctCallbackSearch(data);
}

function fctCallbackSearch(data){
	alert(JSON.stringify(data))
	arreter=true;document.getElementById("loaderProvisoire").parentNode.removeChild(document.getElementById("loaderProvisoire"));montrerResultats("cadreProches",data);carrousel("cadreCoverflow",data);
}

