function chargementBulleInfo(nomDuCadre,idDuFilm){
	if(document.getElementById("bulleInfoExt")){document.getElementById("bulleInfoExt").parentNode.removeChild(document.getElementById("bulleInfoExt"))};
	var bulleInfoExt=document.createElement("div");
	bulleInfoExt.id="bulleInfoExt";
	document.getElementById(nomDuCadre).appendChild(bulleInfoExt);
	bulleInfoExt.style.cssText="width:100%; height:100%; display: none;"	
	var bulleInfo=document.createElement("div");
	bulleInfo.id="bulleInfo";
	document.getElementById("bulleInfoExt").appendChild(bulleInfo);
	bulleInfo.style.cssText="position:relative; width:100%; height:100%; background-color:Silver; border : 1px solid Black;"// border-radius:10px;"
	var conteneurInfo=document.createElement('p');
	conteneurInfo.id="conteneurInfo";
	conteneurInfo.style.cssText='position:absolute; height:90%;top:0px; padding-left:5px;padding-right:5px;text-align: justify;'//border-radius:10px;'
	document.getElementById("bulleInfo").appendChild(conteneurInfo);
	
	var conteneurTitre=document.createElement('p');
	conteneurTitre.style.cssText='float:left;text-align: left;'
	conteneurInfo.appendChild(conteneurTitre)
	var conteneurDateSortie=document.createElement('p');
	conteneurDateSortie.style.cssText='float:left;text-align: left;'
	conteneurInfo.appendChild(conteneurDateSortie)
	var conteneurRealisateur=document.createElement('p');
	conteneurRealisateur.style.cssText='float:left;text-align: left;'
	conteneurInfo.appendChild(conteneurRealisateur)
	var conteneurActeurs=document.createElement('p');
	conteneurActeurs.style.cssText='float:left;text-align: left;'
	conteneurInfo.appendChild(conteneurActeurs)
	var conteneurSynopsis=document.createElement('p');
	conteneurSynopsis.style.cssText='float:left;text-align: justify;'
	conteneurInfo.appendChild(conteneurSynopsis)
	var texteTitre=document.createTextNode("Title");
	conteneurTitre.appendChild(texteTitre)
	var texteDateSortie=document.createTextNode("Release date");
	conteneurDateSortie.appendChild(texteDateSortie)
	var texteRealisateur=document.createTextNode("Director");
	conteneurRealisateur.appendChild(texteRealisateur)
	var texteActeurs=document.createTextNode("Actors");
	conteneurActeurs.appendChild(texteActeurs)
	var texteSynopsis=document.createTextNode("Plot");
	conteneurSynopsis.appendChild(texteSynopsis)
	
	
	/*var texteInfo=document.createTextNode("");
	texteInfo.id="texteInfo";

	texteInfo.textContent=("Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Le film choisi est : "+idDuFilm)
	document.getElementById("bulleInfo").appendChild(conteneurInfo);
	document.getElementById("conteneurInfo").appendChild(texteInfo);*/
	$("#bulleInfoExt").fadeIn(1000);
}

