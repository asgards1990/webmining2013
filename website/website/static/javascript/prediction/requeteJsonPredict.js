// -*- coding: utf-8 -*-
var requete;
var nbactors_min=1;
var nbactors_ok=3;
var nbactors_max=100;
var nbgenres_min=1;
var nbgenres_max=2;
var nbkeywords_min=0;
var nbkeywords_ok=5;
var nbdirector_min=1;
var nbactors=0;
var nbgenres=0;
var nbkeywords=0;
var nbdirector=0;


function verifSiRequete(){
	nbactors=document.getElementById("id_actors-deck").getElementsByClassName("hilight").length;
	nbgenres=0;
	if(document.getElementById("id_genre1-deck").getElementsByClassName("div hilight").length>0){
		nbgenres=nbgenres+1;
	}
	if(document.getElementById("id_genre2-deck").getElementsByClassName("div hilight").length>0){
		nbgenres=nbgenres+1;
	}
	nbkeywords=document.getElementById("id_keyword-deck").getElementsByClassName("div hilight").length;
	nbdirector=document.getElementById("id_directors-deck").getElementsByClassName("hilight").length;
	
	if (nbactors<nbactors_min || nbactors > nbactors_max){
	document.getElementById("prediction_item_actors").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/red2.png')";
	//document.getElementById("prediction_item_actors").getElementsByTagName("div")[0].style.backgroundColor="rgba(0,0,0,0)"
	}
	else{
		if(nbactors<nbactors_ok){
		document.getElementById("prediction_item_actors").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/orange2.png')";
		}
		else{
		document.getElementById("prediction_item_actors").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/green2.png')";
		}
	}
	if (nbdirector<nbdirector_min){
		document.getElementsByClassName("itemDirector")[0].getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/red2.png')";
	}
	else{
		document.getElementsByClassName("itemDirector")[0].getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/green2.png')";
	}
	if(nbgenres<nbgenres_min){
		document.getElementById("prediction_item_genres").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/red2.png')";
	}
	else{
		if(nbgenres<nbgenres_max){
		document.getElementById("prediction_item_genres").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/orange2.png')";
		}
		else{
		document.getElementById("prediction_item_genres").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/green2.png')";
		}
	}
	if(nbkeywords<nbkeywords_ok){
	document.getElementById("prediction_item_keyword").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/orange2.png')";
	}
	else{
	document.getElementById("prediction_item_keyword").getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/green2.png')";
	}
	if(nbactors>=nbactors_min && nbactors<=nbactors_max && nbgenres>=nbgenres_min && nbgenres<=nbgenres_max && nbkeywords>=nbkeywords_min && nbdirector>=nbdirector_min){
		return true;
	}
	else{
		return false;
	}
}

function changementPredict(){
	//verifSiRequete()
	//console.log(JSON.stringify(genererRequetePredict()))
	if(verifSiRequete()){
		envoiDeLaRequetePredict()
	}
}


$(document).ready(function(){
	//$("#results").click(function(){$("#prizestable tbody").empty();})
	//$("#results").click(function(){changementPredict()})
	//$("#id_actors_text").change(function(){console.log(document.getElementById("id_actors-deck").getElementsByClassName("hilight")[0].id)})
	$("#id_actors-deck").bind("DOMSubtreeModified",function(){changementPredict()})
	$("#id_directors-deck").bind("DOMSubtreeModified",function(){changementPredict()})
	$("#id_genre1-deck").bind("DOMSubtreeModified",function(){changementPredict()})
	$("#id_genre2-deck").bind("DOMSubtreeModified",function(){changementPredict()})
	$("#id_keyword-deck").bind("DOMSubtreeModified",function(){changementPredict()})
	$( "#slider-range-min" ).on( "slidechange", function( event, ui ) {changementPredict(); document.getElementsByClassName("item5")[0].getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/green2.png')";} );
	$(".iCheck-helper").click(function(){changementPredict();document.getElementsByClassName("item6")[0].getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/green2.png')";});
	verifSiRequete()
	document.getElementsByClassName("item5")[0].getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/orange2.png')";
	document.getElementsByClassName("item6")[0].getElementsByTagName("div")[0].style.backgroundImage="url('../pesto/static/img/prediction/orange2.png')";
})


function genererRequetePredict(){
	var requestInter=new Object();
	if(nbactors!=0){
		requestInter.actors=new Array();
		for(var i=0;i<document.getElementById("id_actors-deck").getElementsByClassName("hilight").length;i++){
			requestInter.actors[i]=document.getElementById("id_actors-deck").getElementsByClassName("hilight")[i].id;
		}
	}

	if (nbgenres!=0){
		requestInter.genres=new Array();
		var texte1="";
		var texte2="";
		if(document.getElementById("id_genre1-deck").getElementsByClassName("div hilight").length>0){
			for (var i = 0; i < document.getElementById("id_genre1-deck").getElementsByClassName("div hilight")[0].childNodes.length; i++){
				if (document.getElementById("id_genre1-deck").getElementsByClassName("div hilight")[0].childNodes[i].nodeType == 3){
					texte1 = document.getElementById("id_genre1-deck").getElementsByClassName("div hilight")[0].childNodes[i].textContent.trim();
				}
			}
		}
		if(document.getElementById("id_genre2-deck").getElementsByClassName("div hilight").length>0){
			for (var i = 0; i < document.getElementById("id_genre2-deck").getElementsByClassName("div hilight")[0].childNodes.length; i++){
				if (document.getElementById("id_genre2-deck").getElementsByClassName("div hilight")[0].childNodes[i].nodeType == 3){
					texte2 = document.getElementById("id_genre2-deck").getElementsByClassName("div hilight")[0].childNodes[i].textContent.trim();
				}
			}
		}
		//alert(texte1 + texte2)
		compteur=0;
		if (texte1!=""){
			requestInter.genres[compteur]=texte1;
			compteur=compteur+1;
		}
		if (texte2!=""){
			requestInter.genres[compteur]=texte2;
			compteur=compteur+1;
		}

		/*for(var i=0;i<document.getElementById("genre").getElementsByClassName("genre").length;i++){
			requestInter.genres[i]=document.getElementById("genre").getElementsByClassName("genre")[i].value;
			}*/
		}

		if (nbkeywords!=0){
			requestInter.keywords=new Array();
			for(var i=0;i<document.getElementById("id_keyword-deck").getElementsByClassName("div hilight").length;i++){
				requestInter.keywords[i]=document.getElementById("id_keyword-deck").getElementsByClassName("hilight")[i].textContent.replace('X\n','').trim();
			}
		}

		if (nbdirector!=0){
			requestInter.directors=new Array();
			for(var i=0;i<document.getElementById("id_directors-deck").getElementsByClassName("hilight").length;i++){
				requestInter.directors[i]=document.getElementById("id_directors-deck").getElementsByClassName("hilight")[i].id;
			}
		}

		requestInter.budget=parseInt($("#slider-range-min").slider("option", "value"));
		requestInter.release_period=new Object();
		if(document.getElementById("release").getElementsByClassName("checked").length>0){
			requestInter.release_period.season=document.getElementById("release").getElementsByClassName("checked")[0].parentNode.textContent.trim().toLowerCase();
		}
		else{
			requestInter.release_period.season="no-season";
		}

		return requestInter;
	}

	function envoiDeLaRequetePredict(){
		arreter=false;
		console.log(JSON.stringify(genererRequetePredict()))
		if (requete!=undefined){
			requete.abort();
			unloadChargement("results");
		}
		loadChargement("results");
		
		requete=$.post("http://www.prodbox.co/learning/predict/","json_request="+JSON.stringify(genererRequetePredict()),fctCallbackPredict,"json")
		//alert("hello")
		//alert(JSON.stringify(genererRequetePredict()))
		//$.post("http://www.prodbox.co/learning/predict/","json_request="+JSON.stringify(genererRequetePredict()),fctCallbackPredict,"json")
		/*var data=new Object;
		data.success=true;
		data.error="";
		data.prizes_win=new Array;
		data.prizes_win[0]=new Object;
		data.prizes_nomination=new Array;
		data.prizes_nomination[0]=new Object;
		data.prizes_win[0].institution="Festival du film de Berlin"
		//data.prizes_win[0].win="true"
		data.prizes_win[0].value=0.3;
		data.prizes_nomination[0].institution="Oscars"
		//data.prizes_nomination[0].win="false"
		data.prizes_nomination[0].value=0.7;
		data.general_box_office=new Object;
		data.general_box_office.rank=24;
		data.general_box_office.value=320;
		data.general_box_office.neighbors=new Array;
		data.general_box_office.neighbors[0]=new Object;
		data.general_box_office.neighbors[1]=new Object;
		data.general_box_office.neighbors[0].rank=23;
		data.general_box_office.neighbors[0].english_title="Iron Man 3";
		data.general_box_office.neighbors[0].value=325.5;
		data.general_box_office.neighbors[1].rank=25;
		data.general_box_office.neighbors[1].english_title="Le guerrier silencieux";
		data.general_box_office.neighbors[1].value=0.01;
		data.genre_box_office=new Object;
		data.genre_box_office.rank=15;
		data.genre_box_office.value=320;
		data.genre_box_office.neighbors=new Array;
		data.genre_box_office.neighbors[0]=new Object;
		data.genre_box_office.neighbors[1]=new Object;
		data.genre_box_office.neighbors[0].rank=14;
		data.genre_box_office.neighbors[0].english_title="La Dolce Vita";
		data.genre_box_office.neighbors[0].value=325.5;
		data.genre_box_office.neighbors[1].rank=16;
		data.genre_box_office.neighbors[1].english_title="Gravity";
		data.genre_box_office.neighbors[1].value=300;
		data.critics=new Object;
		data.critics.average=0.65147;
		data.critics.reviews=new Array;
		data.critics.reviews[0]=new Object;
		data.critics.reviews[0].journal="T�l�rama";
		data.critics.reviews[0].grade=0.6;
		data.critics.reviews[0].keywords=new Array;
		data.critics.reviews[0].keywords[0]="Insignifiant";
		data.critics.reviews[0].keywords[1]="Path�tique";
		data.critics.reviews[1]=new Object;
		data.critics.reviews[1].journal="Le Monde";
		data.critics.reviews[1].grade=0.4;
		data.critics.reviews[1].keywords=new Array;
		data.critics.reviews[1].keywords[0]="S�rieux";
		data.critics.reviews[1].keywords[1]="Appliqu�";
		data.critics.reviews[2]=new Object;
		data.critics.reviews[2].journal="T�l� 7-Jours";
		data.critics.reviews[2].grade=0.18;
		data.critics.reviews[2].keywords=new Array;
		data.critics.reviews[2].keywords[0]="Eblouissant";
		data.critics.reviews[2].keywords[1]="Un chef d'oeuvre";
		data.critics.reviews[3]=new Object;
		data.critics.reviews[3].journal="T�l� 7-Jours";
		data.critics.reviews[3].grade=0.18;
		data.critics.reviews[3].keywords=new Array;
		data.critics.reviews[3].keywords[0]="Eblouissant";
		data.critics.reviews[3].keywords[1]="Un chef d'oeuvre";
		data.critics.reviews[4]=new Object;
		data.critics.reviews[4].journal="T�l� 7-Jours";
		data.critics.reviews[4].grade=0.18;
		data.critics.reviews[4].keywords=new Array;
		data.critics.reviews[4].keywords[0]="Eblouissant";
		data.critics.reviews[4].keywords[1]="Un chef d'oeuvre";
		data.bag_of_words=new Array;
		data.bag_of_words[0]=new Object;
		data.bag_of_words[0].word="Amazing";
		data.bag_of_words[0].value=0.6;
		data.bag_of_words[1]=new Object;
		data.bag_of_words[1].word="Transcendant";
		data.bag_of_words[1].value=0.3;
		data.bag_of_words[2]=new Object;
		data.bag_of_words[2].word="Shame";
		data.bag_of_words[2].value=0.2;
		data.bag_of_words[3]=new Object;
		data.bag_of_words[3].word="Beautiful";
		data.bag_of_words[3].value=0.7;
		data.bag_of_words[4]=new Object;
		data.bag_of_words[4].word="Blockbuster";
		data.bag_of_words[4].value=0.9;
		data.bag_of_words[5]=new Object;
		data.bag_of_words[5].word="Disappointing";
		data.bag_of_words[5].value=0.1;
		data.bag_of_words[6]=new Object;
		data.bag_of_words[6].word="Firework";
		data.bag_of_words[6].value=0.05;
		data.bag_of_words[7]=new Object;
		data.bag_of_words[7].word="Twinkling";
		data.bag_of_words[7].value=0.95;
		data.bag_of_words[8]=new Object;
		data.bag_of_words[8].word="Promising";
		data.bag_of_words[8].value=0.45;
		data.bag_of_words[9]=new Object;
		data.bag_of_words[9].word="Waste of time";
		data.bag_of_words[9].value=0.5;
	
		fctCallbackPredict(data);*/
		
	}

	function chercherTitre(data, position, rang, type){
		//alert(position + " "+ rang + " "+ type)
		if (type=="general"){
			if (position=="haut"){
				var repRang=-1;
				var rep=-1;
				for(var i=0;i<data.general_box_office.neighbors.length;i++){
					if(data.general_box_office.neighbors[i].rank>repRang && data.general_box_office.neighbors[i].rank<rang){
						repRang=data.general_box_office.neighbors[i].rank;
						rep=i;
					}
				}
				if(rep==-1){return "";}
				else{
					return data.general_box_office.neighbors[rep].rank + " - " + data.general_box_office.neighbors[rep].original_title + " - $ " + data.general_box_office.neighbors[rep].value + " M";
				}
			}
			else{
				var repRang=-1;
				var rep=-1;
				for(var i=0;i<data.general_box_office.neighbors.length;i++){
					if((repRang=-1 || data.general_box_office.neighbors[i].rank<repRang) && data.general_box_office.neighbors[i].rank>rang){
						repRang=data.general_box_office.neighbors[i].rank;
						rep=i;
					}
				}
				if(rep==-1){return "";}
				else{
					return data.general_box_office.neighbors[rep].rank + " - " + data.general_box_office.neighbors[rep].original_title + " - $ " + data.general_box_office.neighbors[rep].value + " M";
				}
			}
		}
		else{
			if (position=="haut"){
				var repRang=-1;
				var rep=-1;
				for(var i=0;i<data.genre_box_office.neighbors.length;i++){
					if(data.genre_box_office.neighbors[i].rank>repRang && data.genre_box_office.neighbors[i].rank<rang){
						repRang=data.genre_box_office.neighbors[i].rank;
						rep=i;
					}
				}
				if(rep==-1){return "";}
				else{
					return data.genre_box_office.neighbors[rep].rank + " - " + data.genre_box_office.neighbors[rep].original_title + " - $ " + data.genre_box_office.neighbors[rep].value + " M";
				}
			}
			else{
				var repRang=-1;
				var rep=-1;
				for(var i=0;i<data.genre_box_office.neighbors.length;i++){
					if((repRang=-1 || data.genre_box_office.neighbors[i].rank<repRang) && data.genre_box_office.neighbors[i].rank>rang){
						repRang=data.genre_box_office.neighbors[i].rank;
						rep=i;
					}
				}
				if(rep==-1){return "";}
				else{
					return data.genre_box_office.neighbors[rep].rank + " - " + data.genre_box_office.neighbors[rep].original_title + " - $ " + data.genre_box_office.neighbors[rep].value + " M";
				}
			}
		}
	}

	//var inter = document.createElement("tr");
	//document.getElementById("prizestable").getElementsByTagName("tbody").appendChild(inter);
	//var institution = document.createElement("tr");
	
	function tousSontRemplis(type){
		if (type=="win"){
			for(var i = 1;i<document.getElementById("prizestable").getElementsByTagName("tr").length;i++){
				if(document.getElementById("prizestable").getElementsByTagName("tr")[i].getElementsByClassName("probav")[0].textContent==""){
					return false;
				}
			}
			return true;
		}
		else{
			for(var i = 1;i<document.getElementById("prizestable").getElementsByTagName("tr").length;i++){
				if(document.getElementById("prizestable").getElementsByTagName("tr")[i].getElementsByClassName("proban")[0].textContent==""){
					return false;
				}
			}
			return true;
		}
	}
	
	function premierePlaceDispo(type){
		if (type=="win"){
			for(var i = 1;i<document.getElementById("prizestable").getElementsByTagName("tr").length;i++){
				if(document.getElementById("prizestable").getElementsByTagName("tr")[i].getElementsByClassName("probav")[0].textContent==""){
					return i;
				}
			}
			return -1;
		}
		else{
			for(var i = 1;i<document.getElementById("prizestable").getElementsByTagName("tr").length;i++){
				if(document.getElementById("prizestable").getElementsByTagName("tr")[i].getElementsByClassName("proban")[0].textContent==""){
					return i;
				}
			}
			return -1;
		}
	}
	
	function tropElements(){
		if(document.getElementById("prizestable").getElementsByTagName("tr").length>=9){
			return true;
		}
		else{
			return false
		}
	}
	
	function creerNouvelElement(type, institution, valeur){
		if (tropElements()==false){
			if (type=="win"){
				var inter = document.createElement("tr");
				document.getElementById("prizestable").getElementsByTagName("tbody")[0].appendChild(inter);
				var institution1 = document.createElement("td");
				institution1.className="institution";
				inter.appendChild(institution1);
				var proban = document.createElement("td");
				proban.className="proban";
				inter.appendChild(proban);
				var institution2 = document.createElement("td");
				institution2.className="institution";
				inter.appendChild(institution2);
				var texteInstitution=document.createTextNode(institution);
				institution2.appendChild(texteInstitution);
				var probav = document.createElement("td");
				probav.className="probav";
				inter.appendChild(probav);
				var texteValeur=document.createTextNode(valeur);
				probav.appendChild(texteValeur);
			}
			else{
				var inter = document.createElement("tr");
				document.getElementById("prizestable").getElementsByTagName("tbody")[0].appendChild(inter);
				var institution1 = document.createElement("td");
				institution1.className="institution";
				inter.appendChild(institution1);
				var texteInstitution=document.createTextNode(institution);
				institution1.appendChild(texteInstitution);
				var proban = document.createElement("td");
				proban.className="proban";
				inter.appendChild(proban);
				var texteValeur=document.createTextNode(valeur);
				proban.appendChild(texteValeur);
				var institution2 = document.createElement("td");
				institution2.className="institution";
				inter.appendChild(institution2);
				var probav = document.createElement("td");
				probav.className="probav";
				inter.appendChild(probav);		
			}
		}
	}
	
	function rajouterDonnees(type,place,institution,valeur){
		if(type=="win"){
			var texteInstitution=document.createTextNode(institution);
			document.getElementById("prizestable").getElementsByTagName("tr")[place].getElementsByClassName("institution")[1].appendChild(texteInstitution);
			var texteValeur=document.createTextNode(valeur);
			document.getElementById("prizestable").getElementsByTagName("tr")[place].getElementsByClassName("probav")[0].appendChild(texteValeur);
		}
		else{
			var texteInstitution=document.createTextNode(institution);
			document.getElementById("prizestable").getElementsByTagName("tr")[place].getElementsByClassName("institution")[0].appendChild(texteInstitution);
			var texteValeur=document.createTextNode(valeur);
			document.getElementById("prizestable").getElementsByTagName("tr")[place].getElementsByClassName("proban")[0].appendChild(texteValeur);
		}
	}
	
	/*function rajouterCritiques(journal, notation){
		var texteJournal=document.createTextNode(journal);
		document.getElementById("reviewstable").
		var texteNotation=document.createTextNode(notation);
		document.getElementById("reviewstable").
	}*/
	
	function fctCallbackPredict(data){
		unloadChargement("results");
		console.log(JSON.stringify(data))
		if(data.success==true){
			/*for(var i=0;i<data.prizes.length;i++){
				var pourcent=Math.round(data.prizes[i].value*10000)/100+" %";
				if(data.prizes[i].win=="true"){
					if(tousSontRemplis("win")==true){
						creerNouvelElement("win",data.prizes[i].institution,pourcent)
					}
					else{
						rajouterDonnees("win",premierePlaceDispo("win"),data.prizes[i].institution,pourcent)
					}
				}
				else{
					if(tousSontRemplis("nomination")==true){
						creerNouvelElement("nomination",data.prizes[i].institution,pourcent)
					}
					else{
						rajouterDonnees("nomination",premierePlaceDispo("nomination"),data.prizes[i].institution,pourcent)
					}
				}
			}*/
			$("#prizestable tbody").empty();
			for(var i=0;i<data.prizes_win.length;i++){
				var pourcent=Math.round(data.prizes_win[i].value*10000)/100+" %";
				if(tousSontRemplis("win")==true){
					creerNouvelElement("win",data.prizes_win[i].institution,pourcent)
				}
				else{
					rajouterDonnees("win",premierePlaceDispo("win"),data.prizes_win[i].institution,pourcent)
				}
			}
			for(var i=0;i<data.prizes_nomination.length;i++){
				var pourcent=Math.round(data.prizes_nomination[i].value*10000)/100+" %";
				if(tousSontRemplis("nomination")==true){
					creerNouvelElement("nomination",data.prizes_nomination[i].institution,pourcent)
				}
				else{
					rajouterDonnees("nomination",premierePlaceDispo("nomination"),data.prizes_nomination[i].institution,pourcent)
				}
			}
			//for(var i=0;i<data.critics.reviews.length;i++){
				//rajouterCritiques(data.critics.reviews[i].journal,data.critics.reviews[i].grade)
			//}
			var lengthOfReviews = data.critics.reviews.length;
				document.getElementById("reviewstable").children[1].children[0].children[0].textContent="Average rating";
				document.getElementById("reviewstable").children[1].children[0].children[1].textContent=Math.round(data.critics.average*100)+"/100";
				
			for (k=0;k<Math.min(data.critics.reviews.length,7);k++) {   
				document.getElementById("reviewstable").children[1].children[k+1].children[0].textContent=data.critics.reviews[k].journal;
				document.getElementById("reviewstable").children[1].children[k+1].children[1].textContent=Math.round(data.critics.reviews[k].grade*100)+"/100";
			};
			
			if (data.general_box_office.rank==1) {
				//affichage des résultats dans le tableau des Box-Office General
				var boxOffice = 0;
				document.getElementById("bogeneraltable").children[1].children[0].children[0].textContent=data.general_box_office.rank;
				document.getElementById("bogeneraltable").children[1].children[0].children[1].textContent="Your movie!";
				boxOffice = Math.round(data.general_box_office.value/10000)/100;
				document.getElementById("bogeneraltable").children[1].children[0].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogeneraltable").children[1].children[1].children[0].textContent=data.general_box_office.neighbors[0].rank;
				document.getElementById("bogeneraltable").children[1].children[1].children[1].textContent=data.general_box_office.neighbors[0].english_title;
				boxOffice = Math.round(data.general_box_office.neighbors[1].value/10000)/100;
				document.getElementById("bogeneraltable").children[1].children[1].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogeneraltable").children[1].children[2].children[0].textContent=data.general_box_office.neighbors[1].rank;
				document.getElementById("bogeneraltable").children[1].children[2].children[1].textContent=data.general_box_office.neighbors[1].english_title;
				boxOffice = Math.round(data.general_box_office.neighbors[2].value/10000)/100;
				document.getElementById("bogeneraltable").children[1].children[2].children[2].textContent="$"+boxOffice+"M";
			
				//affichage des résultats dans le tableau des Box-Office Genre
				document.getElementById("bogenretable").children[1].children[0].children[0].textContent=data.genre_box_office.rank;
				document.getElementById("bogenretable").children[1].children[0].children[1].textContent="Your movie!";
				boxOffice = Math.round(data.general_box_office.value/10000)/100;
				document.getElementById("bogenretable").children[1].children[0].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogenretable").children[1].children[1].children[0].textContent=data.genre_box_office.neighbors[0].rank;
				document.getElementById("bogenretable").children[1].children[1].children[1].textContent=data.genre_box_office.neighbors[0].english_title;
				boxOffice = Math.round(data.genre_box_office.neighbors[0].value/10000)/100;
				document.getElementById("bogenretable").children[1].children[1].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogenretable").children[1].children[2].children[0].textContent=data.genre_box_office.neighbors[1].rank;
				document.getElementById("bogenretable").children[1].children[2].children[1].textContent=data.genre_box_office.neighbors[1].english_title;
				boxOffice = Math.round(data.genre_box_office.neighbors[1].value/10000)/100;
				document.getElementById("bogenretable").children[1].children[2].children[2].textContent="$"+boxOffice+"M";
			}
			else {
				//affichage des résultats dans le tableau des Box-Office General
				var boxOffice = 0;
				document.getElementById("bogeneraltable").children[1].children[1].children[0].textContent=data.general_box_office.rank;
				document.getElementById("bogeneraltable").children[1].children[1].children[1].textContent="Your movie!";
				boxOffice = Math.round(data.general_box_office.value/10000)/100;
				document.getElementById("bogeneraltable").children[1].children[1].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogeneraltable").children[1].children[0].children[0].textContent=data.general_box_office.neighbors[0].rank;
				document.getElementById("bogeneraltable").children[1].children[0].children[1].textContent=data.general_box_office.neighbors[0].english_title.substring(0,35);
				boxOffice = Math.round(data.general_box_office.neighbors[0].value/10000)/100;
				document.getElementById("bogeneraltable").children[1].children[0].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogeneraltable").children[1].children[2].children[0].textContent=data.general_box_office.neighbors[1].rank;
				document.getElementById("bogeneraltable").children[1].children[2].children[1].textContent=data.general_box_office.neighbors[1].english_title.substring(0,35);
				boxOffice = Math.round(data.general_box_office.neighbors[1].value/10000)/100;
				document.getElementById("bogeneraltable").children[1].children[2].children[2].textContent="$"+boxOffice+"M";

				//affichage des résultats dans le tableau des Box-Office Genre
				document.getElementById("bogenretable").children[1].children[1].children[0].textContent=data.genre_box_office.rank;
				document.getElementById("bogenretable").children[1].children[1].children[1].textContent="Your movie!";
				boxOffice = Math.round(data.general_box_office.value/10000)/100;
				document.getElementById("bogenretable").children[1].children[1].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogenretable").children[1].children[0].children[0].textContent=data.genre_box_office.neighbors[0].rank;
				document.getElementById("bogenretable").children[1].children[0].children[1].textContent=data.genre_box_office.neighbors[0].english_title.substring(0,29);
				boxOffice = Math.round(data.genre_box_office.neighbors[0].value/10000)/100;
				document.getElementById("bogenretable").children[1].children[0].children[2].textContent="$"+boxOffice+"M";
				document.getElementById("bogenretable").children[1].children[2].children[0].textContent=data.genre_box_office.neighbors[1].rank;
				document.getElementById("bogenretable").children[1].children[2].children[1].textContent=data.genre_box_office.neighbors[1].english_title.substring(0,29);
				boxOffice = Math.round(data.genre_box_office.neighbors[1].value/10000)/100;
				document.getElementById("bogenretable").children[1].children[2].children[2].textContent="$"+boxOffice+"M";
			};
			
			callback_bag_of_words(data);
		}
	}
	
