function chargementBulleInfo(nomDuCadre,idDuFilm){
	if(document.getElementById("bulleInfoExt")){document.getElementById("bulleInfoExt").parentNode.removeChild(document.getElementById("bulleInfoExt"))};
	var bulleInfoExt=document.createElement("div");
	bulleInfoExt.id="bulleInfoExt";
	document.getElementById(nomDuCadre).appendChild(bulleInfoExt);
	bulleInfoExt.style.cssText="width:100%; height:100%; display: none;"	
	var bulleInfo=document.createElement("div");
	bulleInfo.id="bulleInfo";
	document.getElementById("bulleInfoExt").appendChild(bulleInfo);
	bulleInfo.style.cssText="position:relative; width:100%; height:100%; background-color:Silver; border : 1px solid Black; border-radius:10px;"
	var conteneurInfo=document.createElement('p');
	conteneurInfo.id="conteneurInfo";
	conteneurInfo.style.cssText='margin:0px; position:absolute; height:100%;top:0px; padding-left:5px;padding-right:5px;text-align: justify;'//border-radius:10px;'
	document.getElementById("bulleInfo").appendChild(conteneurInfo);
	
	$.post("/cinema/filmInfo/","film_id="+idDuFilm,function(data){affecter(data)});
	
	function affecter(data){
		var conteneurTitre=document.createElement('p');
		conteneurTitre.style.cssText='margin-left:2px; margin-right:2px; margin-top:4px; margin-bottom:0px;float:left;width:100%;text-align: left;'
		conteneurInfo.appendChild(conteneurTitre)
		var conteneurDateSortie=document.createElement('p');
		conteneurDateSortie.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: left;'
		conteneurInfo.appendChild(conteneurDateSortie)
		var conteneurRealisateur=document.createElement('p');
		conteneurRealisateur.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: left;'
		conteneurInfo.appendChild(conteneurRealisateur)
		var conteneurActeurs=document.createElement('p');
		conteneurActeurs.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: left;'
		conteneurInfo.appendChild(conteneurActeurs)
		var conteneurSynopsis=document.createElement('p');
		conteneurSynopsis.style.cssText='margin-left:2px; margin-right:2px;margin-top:4px;margin-bottom:0px;float:left;width:100%;text-align: justify;'
		conteneurInfo.appendChild(conteneurSynopsis)
		var texteTitre=document.createTextNode("Title : " + data.english_title);
		conteneurTitre.appendChild(texteTitre)
		var texteDateSortie=document.createTextNode("Release date : " + data.release_date);
		conteneurDateSortie.appendChild(texteDateSortie)
		/*var texteRealisateur=document.createTextNode("Director : " + data.release_date);
		conteneurRealisateur.appendChild(texteRealisateur)*/
		var texteActeurs=document.createTextNode("");
		var stringActors="Actors : ";
		for(var i=0; i<data.actors.length;i++){
			stringActors=stringActors+data.actors[i].name;
			if(i!=data.actors.length-1){
				stringActors=stringActors+", ";
			}
		}
		conteneurActeurs.appendChild(texteActeurs)
		texteActeurs.textContent=stringActors;
		var texteSynopsis=document.createTextNode("Plot : " + data.plot);
		conteneurSynopsis.appendChild(texteSynopsis)
		$("#bulleInfoExt").fadeIn(1000);
	}
}

