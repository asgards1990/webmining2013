var requete;

function verifAuMoinsUnCrit(){
	if($("#acteurs").prop("checked")==true || $("#genre").prop("checked")==true || $("#budgets").prop("checked")==true || $("#review").prop("checked")==true){
		return true;
	}
	else{
		return false;
	}
}

function changement(){
	if(verifAuMoinsUnCrit()==true){
		$.post("http://localhost:8000/cinema/getId/","film_name="+"Avatar",function(data){envoiDeLaRequeteSearch(data);});
		//envoiDeLaRequeteSearch(nomfilm);
	}
	else{
		alert("Please select at least one criterion.")
	}
	//$.post("http://localhost:8000/cinema/filmInfo/","film_id=tt0499549",function(data){alert($.parseJSON(data).etitle)}); //$.parseJSON(data).plot
        //alert('hello');
       //$.post("http://localhost:8000/cinema/filmInfo/","film_id=tt0899128",function(data){console.log(data.actors[0].imdb_id)}); 
	   $.post("http://localhost:8000/cinema/getId/","film_name="+"Avatar",function(data){console.log(data)}); 
}

$(document).ready(function(){

$(".checkbox").change(function(){changement();})
$(".iCheck-helper").click(function(){changement();})
$("#rateit").click(function(){changement();})
$( "#slider-range" ).on( "slidechange", function( event, ui ) {changement();} );
$( "#slider-rangeyear" ).on( "slidechange", function( event, ui ) {changement();} );
})


function genererRequeteSearch(nomfilm){
	var requestInter=new Object();
	requestInter.id=nomfilm;//document.getElementById("moviesearch").children[0].id;
	requestInter.nbresults=10;
	requestInter.criteria=new Object();
	requestInter.criteria.actor_director=$("#acteurs").prop("checked");
	requestInter.criteria.genre=$("#genre").prop("checked");
	requestInter.criteria.budget=$("#budgets").prop("checked");
	requestInter.criteria.review=$("#review").prop("checked");
	requestInter.filter=new Object();
	var compteur=0;
	for(var i=0;i<document.getElementById("actors").getElementsByClassName("listactor").length;i++){
		if (document.getElementById("actors").getElementsByClassName("listactor")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
			compteur=compteur+1;
		}
	}
	if(compteur>0){
		requestInter.filter.actors=new Array();
		var compteur=0;
		for(var i=0;i<document.getElementById("actors").getElementsByClassName("listactor").length;i++){
			if (document.getElementById("actors").getElementsByClassName("listactor")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
				requestInter.filter.actors[compteur]=document.getElementById("actors").getElementsByClassName("listactor")[i].children[0].id;
				compteur=compteur+1;
			}
		}
	}
	var compteur=0;
	for(var i=0;i<document.getElementById("actors").getElementsByClassName("listdirector").length;i++){
		if (document.getElementById("actors").getElementsByClassName("listdirector")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
			compteur=compteur+1;
		}
	}
	if(compteur>0){
		requestInter.filter.directors=new Array();
		compteur=0;
		for(var i=0;i<document.getElementById("actors").getElementsByClassName("listdirector").length;i++){
			if (document.getElementById("actors").getElementsByClassName("listdirector")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
				requestInter.filter.directors[compteur]=document.getElementById("actors").getElementsByClassName("listdirector")[i].children[0].id;
				compteur=compteur+1;
			}
		}
	}
	var compteur=0;
	for(var i=0;i<document.getElementById("genres").getElementsByClassName("listgenre").length;i++){
		if (document.getElementById("genres").getElementsByClassName("listgenre")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
			compteur=compteur+1;
		}
	}
	if(compteur>0){
		requestInter.filter.genres=new Array();
		compteur=0;
		for(var i=0;i<document.getElementById("genres").getElementsByClassName("listgenre").length;i++){
			if (document.getElementById("genres").getElementsByClassName("listgenre")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
				requestInter.filter.genres[compteur]=document.getElementById("genres").getElementsByClassName("listgenre")[i].getElementsByClassName("icheckbox_line-red")[0].textContent;
				compteur=compteur+1;
			}
		}
	}
	requestInter.filter.budget=new Object();
	requestInter.filter.budget.min=parseInt(document.getElementById("amount").value.slice(1,document.getElementById("amount").value.slice(1,-1).indexOf("-")-1));
	requestInter.filter.budget.max=parseInt(document.getElementById("amount").value.slice(document.getElementById("amount").value.slice(1,-1).indexOf("-")+4,-1));
	requestInter.filter.release_period=new Object();
	requestInter.filter.release_period.begin=parseInt(document.getElementById("amountyear").value.slice(0,document.getElementById("amount").value.slice(1,-1).indexOf("-")+1));
	requestInter.filter.release_period.end=parseInt(document.getElementById("amountyear").value.slice(document.getElementById("amount").value.slice(1,-1).indexOf("-")+4));
	requestInter.filter.reviews=new Object();
	requestInter.filter.reviews.min=parseInt(document.getElementById("rateit-range-2").getAttribute("aria-valuenow"));
	return requestInter;
}

function envoiDeLaRequeteSearch(nomfilm){
	arreter=false;
	console.log(JSON.stringify(genererRequeteSearch(nomfilm)))
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
	data.results[2].title="Thor: Le Monde des T�n�bres";
	data.results[2].value=0.5;
	data.results[3]=new Object;
	data.results[3].id="tt0816442";
	data.results[3].title="La Voleuse de livres";
	data.results[3].value=0;
	fctCallbackSearch(data);*/
}

function fctCallbackSearch(data){
	console.log(JSON.stringify(data))
	unloadChargement("sousCadreResultats");
	$("#cadreProches").empty();
	$("#cadreCoverflow").empty();
	montrerResultats("cadreProches",data);
	carrousel("cadreCoverflow",data);
}

