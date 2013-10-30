function chargementBulleInfo(nomDuCadre,idDuFilm){
	if(document.getElementById("bulleInfoExt")){document.getElementById("bulleInfoExt").parentNode.removeChild(document.getElementById("bulleInfoExt"))};
	var bulleInfoExt=document.createElement("div");
	bulleInfoExt.id="bulleInfoExt";
	document.getElementById(nomDuCadre).appendChild(bulleInfoExt);
	bulleInfoExt.style.cssText="width:100%; height:100%; display: none;"	
	var bulleInfo=document.createElement("div");
	bulleInfo.id="bulleInfo";
	document.getElementById("bulleInfoExt").appendChild(bulleInfo);
	bulleInfo.style.cssText="width:100%; height:100%; background-color:Silver; display: table;border : 1px solid Black; border-radius:10px;"
	var conteneurInfo=document.createElement('p');
	conteneurInfo.id="conteneurInfo";

	conteneurInfo.style.cssText='display: table-cell; padding-top:5px; padding-left:5px;padding-right:5px;text-align: justify;' 

	var texteInfo=document.createTextNode("");
	texteInfo.id="texteInfo";

	texteInfo.textContent=("Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Ceci est du blabla! Le film choisi est : "+idDuFilm)
	document.getElementById("bulleInfo").appendChild(conteneurInfo);
	document.getElementById("conteneurInfo").appendChild(texteInfo);
	$("#bulleInfoExt").fadeIn(1000);
}

