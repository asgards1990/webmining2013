var requete;

function changement(){
	envoiDeLaRequeteSearch();
	//$.post("http://localhost:8000/cinema/filmInfo/","film_id=tt0499549",function(data){alert($.parseJSON(data).etitle)}); //$.parseJSON(data).plot
        //alert('hello');
       $.post("http://localhost:8000/cinema/filmInfo/","film_id=tt0899128",function(data){console.log(data.actors[0].imdb_id)}); 
}


$(document).ready(function(){

$(".checkbox").change(function(){changement();})
$(".iCheck-helper").click(function(){changement();})
$("#rateit").click(function(){changement();})
$( "#slider-range" ).on( "slidechange", function( event, ui ) {changement();} );
$( "#slider-rangeyear" ).on( "slidechange", function( event, ui ) {changement();} );

})


function genererRequeteSearch(){
	var requestInter=new Object();
	requestInter.id="tt1024648";//document.getElementById("moviesearch").children[0].id;
	requestInter.nbresults=10;
	requestInter.criteria=new Object();
	requestInter.criteria.actor_director=$("#acteurs").prop("checked");
	requestInter.criteria.genre=$("#genre").prop("checked");
	requestInter.criteria.budget=$("#budgets").prop("checked");
	requestInter.criteria.review=$("#review").prop("checked");
	/*requestInter.filter=new Object();
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
	/*requestInter.filter.genres=new Array();
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
	arreter=false;
	console.log(JSON.stringify(genererRequeteSearch()))
	if (requete!=undefined){
		requete.abort();
		unloadChargement("sousCadreResultats");
	}
	loadChargement("sousCadreResultats");
	requete=$.post("http://senellart.com:8080/search/","json_request="+JSON.stringify(genererRequeteSearch()),fctCallbackSearch,"json")
	/*var data=new Object;
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
	fctCallbackSearch(data);*/
}

function fctCallbackSearch(data){
	console.log(JSON.stringify(data))
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

