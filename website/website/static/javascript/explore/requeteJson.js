var requete;

function changement(){
	envoiDeLaRequeteSearch();
	//setTimeout(function(){unloadChargement("sousCadreResultats")},2000)
	/*if (requete!=undefined){
	requete.abort();
	}
	//alert("!!!")
	requete=$.get("http://www.omdbapi.com/?i=" + "tt1951264", function(data){alert(data)})
	if (requete!=undefined){
	requete.abort();
	}
	//alert("!!!")
	requete=$.get("http://www.omdbapi.com/?i=" + "tt2294629", function(data){alert(data)})
	if (requete!=undefined){
	requete.abort();
	}
	//alert("!!!")
	requete=$.get("http://www.omdbapi.com/?i=" + "tt1981115", function(data){alert(data)})*/
}


$(document).ready(function(){
//envoiDeLaRequete()
//alert("hello")
$(".checkbox").change(function(){changement();})
$(".iCheck-helper").click(function(){changement();})

//document.getElementById("amount").onchange=function(){alert("!!!")};//change(function(){alert("checkbox truc3!!!")})
$( "#slider-range" ).on( "slidechange", function( event, ui ) {changement();} );
//setTimeout(function(){envoiDeLaRequeteSearch();},1000)
//setTimeout(function(){envoiDeLaRequetePredict()},1000)
//$("#title").click(function(){envoiDeLaRequeteSearch()})
//$("#title").click(function(){envoiDeLaRequetePredict()})
})


function genererRequeteSearch(){
	var requestInter=new Object();
	requestInter.id=document.getElementById("moviesearch").children[0].id;
	requestInter.nbresults=10;
	requestInter.criteria=new Object();
	requestInter.criteria.actor_director=$("#acteurs").prop("checked");
	requestInter.criteria.genre=$("#genre").prop("checked");
	requestInter.criteria.budget=$("#budgets").prop("checked");
	requestInter.criteria.review=$("#review").prop("checked");
	requestInter.filter=new Object();
	requestInter.filter.actors=new Array();
	var compteur=0;
	/*for(var i=0;i<document.getElementById("actors").getElementsByClassName("actor").length;i++){
		if (document.getElementById("actors").getElementsByClassName("actor")[i].children[0].checked==true){
			requestInter.filter.actors[compteur]=document.getElementById("actors").getElementsByClassName("actor")[i].children[1].id;
			compteur=compteur+1;
		}
	}*/
	/*requestInter.filter.directors=new Array();
	compteur=0;
	for(var i=0;i<document.getElementById("actors").getElementsByClassName("director").length;i++){
		if (document.getElementById("actors").getElementsByClassName("director")[i].children[0].checked==true){
			requestInter.filter.directors[compteur]=document.getElementById("actors").getElementsByClassName("director")[i].children[1].id;
			compteur=compteur+1;
		}
	}*/
	requestInter.filter.genres=new Array();
	compteur=0;
	for(var i=0;i<document.getElementById("genres").getElementsByClassName("icheckbox_line-red").length;i++){
		//alert("hello")
		if (document.getElementById("genres").getElementsByClassName("icheckbox_line-red")[i].children[0].checked==true){
			requestInter.filter.genres[compteur]=document.getElementById("genres").getElementsByClassName("icheckbox_line-red")[i].textContent;
			compteur=compteur+1;
		}
	}
	requestInter.filter.budget=new Object();
	requestInter.filter.budget.min=document.getElementById("amount").value.slice(1,document.getElementById("amount").value.slice(1,-1).indexOf("-")-1);
	requestInter.filter.budget.max=document.getElementById("amount").value.slice(document.getElementById("amount").value.slice(1,-1).indexOf("-")+4,-1);
	/*requestInter.filter.reviews=new Object();
	requestInter.filter.reviews.min=valueStar;*/
	//requestInter.filter.release_period=new Object();
	//requestInter.filter.release_period.begin="1900-01-01"; //inutile
	//requestInter.filter.release_period.end="2100-01-01"; //inutile
	return requestInter;
}

function envoiDeLaRequeteSearch(){
	//alert("hello")
	arreter=false;
	loadChargement("sousCadreResultats");
	alert(JSON.stringify(genererRequeteSearch()))
	//requete=$.post("http://senellart.com:8080/search/","json_request="+JSON.stringify(genererRequeteSearch()),fctCallbackSearch,"json")
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
	data.results[2].title="Thor: Le Monde des T�n�bres";
	data.results[2].value=0.5;
	data.results[3]=new Object;
	data.results[3].id="tt0816442";
	data.results[3].title="La Voleuse de livres";
	data.results[3].value=0;
	fctCallbackSearch(data);
}

function fctCallbackSearch(data){
	alert(JSON.stringify(data))
	setTimeout(
		function(){
			unloadChargement("sousCadreResultats");
			$("#cadreProches").empty();
			$("#cadreCoverflow").empty();
			montrerResultats("cadreProches",data);
			carrousel("cadreCoverflow",data);
		}
	,1000)
}
