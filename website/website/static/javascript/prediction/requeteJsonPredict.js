var nbactors_min=1;
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
	if(nbactors>=nbactors_min && nbactors<=nbactors_max && nbgenres>=nbgenres_min && nbgenres<=nbgenres_max && nbkeywords>=nbkeywords_min && nbdirector>=nbdirector_min){
		return true;
	}
	else{
		return false;
	}
}

function changementPredict(){
	if(verifSiRequete()){
		$.post("http://senellart.com:8080/predict/","json_request="+JSON.stringify(genererRequetePredict()),function(data){alert(JSON.stringify(data))},"json")
	}
}


$(document).ready(function(){
//loadChargement("results");
//setTimeout(function(){unloadChargement("results");},2000)
//$("#results").click(function(){alert(JSON.stringify(genererRequetePredict()))})

$("#results").click(function(){changementPredict()})
//envoiDeLaRequete()
//alert("hello")
//alert(JSON.stringify(genererRequetePredict()))
//$.post("http://senellart.com:8080/predict/","json_request="+JSON.stringify(genererRequetePredict()),function(data){alert(JSON.stringify(data))},"json")
//setTimeout(function(){envoiDeLaRequetePredict()},1000)
//$("#title").click(function(){envoiDeLaRequetePredict()})

// affichage des nominations dans le tableau des Prizes
document.getElementById("prizestable").children[1].children[0].children[0].textContent="% Festival de Cannes %";
document.getElementById("prizestable").children[1].children[0].children[1].textContent="% 30 %";

// affichage des victoires dans le tableau des Prizes
document.getElementById("prizestable").children[1].children[0].children[2].textContent="% Festival de Cannes %";
document.getElementById("prizestable").children[1].children[0].children[3].textContent="% 10 %";


//affichage des nominations dans le tableau des Prizes (boucle JSON, i allant de 0 à 9)
// document.getElementById("prizestable").children[1].children[i].children[0].textContent="% Festival de Cannes %";
// document.getElementById("prizestable").children[1].children[i].children[1].textContent="% 30 %";

//affichage des résultats dans le tableau des Box-Office General
document.getElementById("bogeneraltable").children[1].children[0].children[0].textContent="% 23 %";
document.getElementById("bogeneraltable").children[1].children[0].children[1].textContent="% Iron Man 3 %";
document.getElementById("bogeneraltable").children[1].children[0].children[2].textContent="% $325.5 M %";

//affichage des résultats dans le tableau des Box-Office General (boucle JSON)
//document.getElementById("bogeneraltable").children[1].children[i].children[0].textContent="% 23 %";
//document.getElementById("bogeneraltable").children[1].children[i].children[1].textContent="% Iron Man 3 %";
//document.getElementById("bogeneraltable").children[1].children[i].children[2].textContent="% $325.5 M %";

//affichage des résultats dans le tableau des Box-Office Genre
document.getElementById("bogenretable").children[1].children[0].children[0].textContent="% 23bis %";
document.getElementById("bogenretable").children[1].children[0].children[1].textContent="% Iron Man 4 %";
document.getElementById("bogenretable").children[1].children[0].children[2].textContent="% $325.6 M %";

//affichage des résultats dans le tableau des Box-Office Genre (boucle JSON)
document.getElementById("bogenretable").children[1].children[0].children[0].textContent="% 23bis %";
document.getElementById("bogenretable").children[1].children[0].children[1].textContent="% Iron Man 4 %";
document.getElementById("bogenretable").children[1].children[0].children[2].textContent="% $325.6 M %";

})


function genererRequetePredict(){
	var requestInter=new Object();
	if(nbactors!=0){
		requestInter.actors=new Array();
		for(var i=0;i<document.getElementById("id_actors-deck").getElementsByClassName("hilight").length;i++){
			requestInter.actors[i]=document.getElementById("id_actors-deck").getElementsByClassName("hilight")[i].id;
		}
	}

	if (true || nbgenres!=0){
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

	if (true || nbkeywords!=0){
		requestInter.keywords=new Array();
		for(var i=0;i<document.getElementById("id_keyword-deck").getElementsByClassName("div hilight").length;i++){
			requestInter.keywords[i]=document.getElementById("id_keyword-deck").getElementsByClassName("hilight")[i].textContent.trim();
		}
	}

	if (nbdirector!=0){
		requestInter.directors=new Array();
		for(var i=0;i<document.getElementById("id_directors-deck").getElementsByClassName("hilight").length;i++){
			requestInter.directors[i]=document.getElementById("id_directors-deck").getElementsByClassName("hilight")[i].id;
		}
	}

	requestInter.budget=new Object();
	requestInter.budget.min=parseInt(document.getElementById("amount").value.slice(1,document.getElementById("amount").value.slice(1,-1).indexOf("-")-1));
	requestInter.budget.max=parseInt(document.getElementById("amount").value.slice(document.getElementById("amount").value.slice(1,-1).indexOf("-")+4,-1));
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
	requete=$.post("http://senellart.com:8080/search/","json_request="+JSON.stringify(genererRequeteSearch(nomfilm,init)),fctCallbackSearch,"json")
	//alert("hello")
	//alert(JSON.stringify(genererRequetePredict()))
	//$.post("http://senellart.com:8080/predict/","json_request="+JSON.stringify(genererRequetePredict()),fctCallbackPredict,"json")
	/*var data=new Object;
	data.success=true;
	data.error="";
	data.prizes=new Array;
	data.prizes[0]=new Object;
	data.prizes[1]=new Object;
	data.prizes[0].institution="Festival du film de Berlin"
	data.prizes[0].win="true"
	data.prizes[0].value=0.3;
	data.prizes[1].institution="Oscars"
	data.prizes[1].win="false"
	data.prizes[1].value=0.7;
	data.general_box_office=new Object;
	data.general_box_office.rank=24;
	data.general_box_office.value=320;
	data.general_box_office.neighbors=new Array;
	data.general_box_office.neighbors[0]=new Object;
	data.general_box_office.neighbors[1]=new Object;
	data.general_box_office.neighbors[0].rank=23;
	data.general_box_office.neighbors[0].original_title="Iron Man 3";
	data.general_box_office.neighbors[0].value=325.5;
	data.general_box_office.neighbors[1].rank=25;
	data.general_box_office.neighbors[1].original_title="Le guerrier silencieux";
	data.general_box_office.neighbors[1].value=0.01;
	data.genre_box_office=new Object;
	data.genre_box_office.rank=15;
	data.genre_box_office.value=320;
	data.genre_box_office.neighbors=new Array;
	data.genre_box_office.neighbors[0]=new Object;
	data.genre_box_office.neighbors[1]=new Object;
	data.genre_box_office.neighbors[0].rank=14;
	data.genre_box_office.neighbors[0].original_title="La Dolce Vita";
	data.genre_box_office.neighbors[0].value=325.5;
	data.genre_box_office.neighbors[1].rank=16;
	data.genre_box_office.neighbors[1].original_title="Gravity";
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
	data.bag_of_words[9].value=0.5;*/
	
	fctCallbackPredict(data);
		
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

//function fctCallbackPredict(data){
//	//alert(JSON.stringify(data))
//	var boiteBoxOffice=document.getElementById("boxoffice");
//	var boiteGeneral=document.createElement("div");
//	boiteGeneral.id="boiteGeneral"
//	boiteGeneral.style.cssText="float : left; width:80%; height:30%;border:1px solid Black"
//	boiteBoxOffice.appendChild(boiteGeneral);
//	var titre1=document.createTextNode("G�n�ral");
//	titre1.id="titre1"
//	boiteGeneral.appendChild(titre1);
//	var boiteClassement1=document.createElement("div");
//	boiteClassement1.id="boiteClassement1"
//	boiteClassement1.style.cssText="width:100%; height:70%;border:1px Black solid"
//	boiteGeneral.appendChild(boiteClassement1);
//	var boiteFilmHaut1=document.createElement("div");
//	var boiteFilmMilieu1=document.createElement("div");
//	var boiteFilmBas1=document.createElement("div");
//	boiteFilmHaut1.id="boiteFilmHaut1";
//	boiteFilmHaut1.style.cssText="float : left; width:95%; height:30%;border:1px solid Black;border-radius : 5px;"
//	boiteClassement1.appendChild(boiteFilmHaut1);
//	boiteFilmMilieu1.id="boiteFilmMilieu1";
//	boiteFilmMilieu1.style.cssText="float : left; width:95%; height:30%;border:1px solid Black;border-radius : 5px;"
//	boiteClassement1.appendChild(boiteFilmMilieu1);
//	boiteFilmBas1.id="boiteFilmBas1";
//	boiteFilmBas1.style.cssText="float : left; width:95%; height:30%;border:1px solid Black;border-radius : 5px;"
//	boiteClassement1.appendChild(boiteFilmBas1);
//	var titreFilmHaut1=document.createTextNode("");
//	titreFilmHaut1.textContent=chercherTitre(data, "haut",data.general_box_office.rank , "general");
//	boiteFilmHaut1.appendChild(titreFilmHaut1);
//	var titreFilmMilieu1=document.createTextNode("");
//	titreFilmMilieu1.textContent=data.general_box_office.rank + " - $ " + data.general_box_office.value + " M";
//	boiteFilmMilieu1.appendChild(titreFilmMilieu1);
//	var titreFilmBas1=document.createTextNode("");
//	titreFilmBas1.textContent=chercherTitre(data, "bas",data.general_box_office.rank , "general");
//	boiteFilmBas1.appendChild(titreFilmBas1);
//	
//	var boiteGenre=document.createElement("div");
//	boiteGenre.id="boiteGenre"
//	boiteGenre.style.cssText="float : left; width:80%; height:30%;border:1px Black solid"
//	boiteBoxOffice.appendChild(boiteGenre);
//	var titre2=document.createTextNode("Genre");
//	titre2.id="titre2"
//	boiteGenre.appendChild(titre2);
//	var boiteClassement2=document.createElement("div");
//	boiteClassement2.id="boiteClassement2";
//	boiteClassement2.style.cssText="width:100%; height:70%;border:1px Black solid"
//	boiteGenre.appendChild(boiteClassement2);
//	var boiteFilmHaut2=document.createElement("div");
//	var boiteFilmMilieu2=document.createElement("div");
//	var boiteFilmBas2=document.createElement("div");
//	boiteFilmHaut2.id="boiteFilmHaut2";
//	boiteFilmHaut2.style.cssText="float : left; width:95%; height:30%;border:1px solid Black;border-radius : 5px;"
//	boiteClassement2.appendChild(boiteFilmHaut2);
//	boiteFilmMilieu2.id="boiteFilmMilieu2";
//	boiteFilmMilieu2.style.cssText="float : left; width:95%; height:30%;border:1px solid Black;border-radius : 5px;"
//	boiteClassement2.appendChild(boiteFilmMilieu2);
//	boiteFilmBas2.id="boiteFilmBas2";
//	boiteFilmBas2.style.cssText="float : left; width:95%; height:30%;border:1px solid Black;border-radius : 5px;"
//	boiteClassement2.appendChild(boiteFilmBas2);
//	var titreFilmHaut2=document.createTextNode("");
//	titreFilmHaut2.textContent=chercherTitre(data, "haut",data.genre_box_office.rank , "genre");
//	boiteFilmHaut2.appendChild(titreFilmHaut2);
//	var titreFilmMilieu2=document.createTextNode("");
//	titreFilmMilieu2.textContent=data.genre_box_office.rank + " - $ " + data.genre_box_office.value + " M";
//	boiteFilmMilieu2.appendChild(titreFilmMilieu2);
//	var titreFilmBas2=document.createTextNode("");
//	titreFilmBas2.textContent=chercherTitre(data, "bas",data.genre_box_office.rank , "genre");
//	boiteFilmBas2.appendChild(titreFilmBas2);
//	
//	var boiteReviews=document.getElementById("reviews");
//	var boiteMoyenne=document.createElement("div");
//	boiteMoyenne.id="boiteMoyenne"
//	boiteMoyenne.style.cssText="width:80%; height:30%;border:1px solid Black;"
//	boiteReviews.appendChild(boiteMoyenne);
//	var conteneurNote=document.createElement("div");
//	boiteMoyenne.appendChild(conteneurNote);
//	var note=document.createTextNode((data.critics.average*5+" ").slice(0,3)+"/5");
//	conteneurNote.appendChild(note);
//	var cadreEtoile=document.createElement("canvas");
//	cadreEtoile.style.cssText=""
//	cadreEtoile.id="cadreEtoile";
//	cadreEtoile.setAttribute("width", 250);
//	cadreEtoile.setAttribute("height", 50);
//	boiteMoyenne.appendChild(cadreEtoile);
//	var etoile=new Image();
//	etoile.src="../pesto/static/img/explore/reviews.png"
//	etoile.onload=function(){
//		var width = etoile.width,height = etoile.height;
//        var context = $("#cadreEtoile")[0].getContext("2d");
//		function dessinerLigne(i,translation){
//			return function(){
//				context.setTransform(0.5, 0,0,0.5,0.5*translation, 0);
//            	context.drawImage(etoile,width-i,0,2,height,width-i,0,2,height);	
//			}
//		}
//		function dessinerLigne2(i,translation){
//			return function(){
//				context.setTransform(0.5, 0,0,0.5,0.5*translation, 0);
//            	context.drawImage(etoile,width-i,0,2,height,width-i,0,2,height);	
//			}
//		}
//		var nombreEtoile=Math.floor(data.critics.average*5);
//		var reste=data.critics.average*5-Math.floor(data.critics.average*5);
//		var vitesse=5;
//		var espaceEntreEtoiles=10;
//		for (var j=0;j<nombreEtoile;j++){
//			for (var i = 0; i<=width; ++i) {
//				setTimeout(dessinerLigne(i,j*width+espaceEntreEtoiles),(width-i)*vitesse+width*vitesse*j);
//			}
//		}
//        for (var i = width*(1-reste); i<=width; ++i) {
//            setTimeout(dessinerLigne2(i,nombreEtoile*width+espaceEntreEtoiles),(width-i)*vitesse+width*vitesse*nombreEtoile);
//		}
//	}
//	
//	//arreter=true;document.getElementById("loaderProvisoire").parentNode.removeChild(document.getElementById("loaderProvisoire"));montrerResultats("cadreProches");carrousel("cadreCoverflow");
//}
//
//
