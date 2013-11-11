var requete;
var idFilm;

function verifAuMoinsUnCrit(){
	if($("#acteurs").prop("checked")==true || $("#genre").prop("checked")==true || $("#budgets").prop("checked")==true || $("#review").prop("checked")==true){
		return true;
	}
	else{
		return false;
	}
}

function changement2(){
	$("#acteurs").prop("checked",true);
	$("#genre").prop("checked",true);
	$("#budgets").prop("checked",true);
	$("#review").prop("checked",true);
	var film_imdb_id = $('#id_title_original-deck span.div').attr('data-value');
	envoiDeLaRequeteSearch(film_imdb_id,true);
}

function changement(){
	if(document.getElementById("id_title_original-deck").children.length >0){
		//console.log("hello")
		if(verifAuMoinsUnCrit()==true){
			var film_imdb_id = $('#id_title_original-deck span.div').attr('data-value');
			envoiDeLaRequeteSearch(film_imdb_id,false);
		}
		else{
			alert("Please select at least one criteria.")
		}
	}
	else{
		alert("Please select a film.")
	}
}

$(document).ready(function(){
//chargementBulleInfo("cadreInfo","test")
$(".checkbox").change(function(){changement();})
//$(".iCheck-helper").click(function(){changement();})
$("#rateit").click(function(){changement();})
$( "#slider-range" ).on( "slidechange", function( event, ui ) {changement();} );
$( "#slider-rangeyear" ).on( "slidechange", function( event, ui ) {changement();} );
})


function genererRequeteSearch(nomfilm,init){
	var requestInter=new Object();
	requestInter.id=nomfilm;
	requestInter.nbresults=10;
	if(init==false){
		requestInter.criteria=new Object();
		requestInter.criteria.actor_director=$("#acteurs").prop("checked");
		requestInter.criteria.genre=$("#genre").prop("checked");
		requestInter.criteria.budget=$("#budgets").prop("checked");
		requestInter.criteria.review=$("#review").prop("checked");
		//requestInter.criteria.director=$("#directors").prop("checked");
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
		for(var i=0;i<document.getElementById("directors").getElementsByClassName("listdirector").length;i++){
			if (document.getElementById("directors").getElementsByClassName("listdirector")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
				compteur=compteur+1;
			}
		}
		if(compteur>0){
			requestInter.filter.directors=new Array();
			compteur=0;
			for(var i=0;i<document.getElementById("directors").getElementsByClassName("listdirector").length;i++){
				if (document.getElementById("directors").getElementsByClassName("listdirector")[i].getElementsByClassName("icheckbox_line-red")[0].children[0].checked==true){
						requestInter.filter.directors[compteur]=document.getElementById("directors").getElementsByClassName("listdirector")[i].children[0].id;
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
		requestInter.filter.budget.min=parseFloat(document.getElementById("amount").value.slice(1,document.getElementById("amount").value.slice(1,-1).indexOf("-")-1));
		requestInter.filter.budget.max=parseFloat(document.getElementById("amount").value.slice(document.getElementById("amount").value.slice(1,-1).indexOf("-")+4,-1));
		requestInter.filter.release_period=new Object();
		requestInter.filter.release_period.begin=parseInt(document.getElementById("amountyear").value.slice(0,document.getElementById("amountyear").value.slice(1,-1).indexOf("-")+1));
		requestInter.filter.release_period.end=parseInt(document.getElementById("amountyear").value.slice(document.getElementById("amountyear").value.slice(1,-1).indexOf("-")+2));
		requestInter.filter.reviews=new Object();
		requestInter.filter.reviews.min=parseFloat(document.getElementById("rateit-range-2").getAttribute("aria-valuenow"))/5;
	}
	else{
		requestInter.criteria=new Object();
		requestInter.criteria.actor_director=true;
		//requestInter.criteria.director=true;
		requestInter.criteria.genre=true;
		requestInter.criteria.budget=true;
		requestInter.criteria.review=true;
	}
	return requestInter;
}

function envoiDeLaRequeteSearch(nomfilm,init){
	idFilm=nomfilm;
	arreter=false;
	console.log(JSON.stringify(genererRequeteSearch(nomfilm,init)))
	if (requete!=undefined){
		requete.abort();
		unloadChargement("sousCadreResultats");
	}
	loadChargement("sousCadreResultats");
	requete=$.post("http://www.prodbox.co/learning/search/","json_request="+JSON.stringify(genererRequeteSearch(nomfilm,init)),fctCallbackSearch,"json")
}

function fctCallbackSearch(data){
	console.log(JSON.stringify(data))
	if(data.success==true){
		unloadChargement("sousCadreResultats");
		$("#cadreProches").empty();
		$("#cadreCoverflow").empty();
		montrerResultats("cadreProches",data);
		carrousel("cadreCoverflow",data);
	}
	else{
		console.log(data.error)
		unloadChargement("sousCadreResultats");
	}
}

