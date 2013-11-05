$(document).ready(function(){
//envoiDeLaRequete()
//alert("hello")
setTimeout(function(){envoiDeLaRequetePredict()},1000)
//$("#title").click(function(){envoiDeLaRequetePredict()})
})

function genererRequetePredict(){
	var requestInter=new Object();
	/*requestInter.actors=new Array();
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
	}*/
	//requestInter.budget=10.2;
	//
	//requestInter.release_period=new Object();
	//requestInter.release_period.season="summer";
	//requestInter.language="fr";
	
	return requestInter;
}

function envoiDeLaRequetePredict(){
	//alert("hello")
	alert(JSON.stringify(genererRequetePredict()))
	//$.post("http://senellart.com:8080/predict/","json_request="+JSON.stringify(genererRequetePredict()),fctCallbackPredict,"json")
	var data=new Object;
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
	data.critics.average=0.4;
	data.critics.reviews=new Array;
	data.critics.reviews[0]=new Object;
	data.critics.reviews[0].journal="Télérama";
	data.critics.reviews[0].grade=0.6;
	data.critics.reviews[0].keywords=new Array;
	data.critics.reviews[0].keywords[0]="Insignifiant";
	data.critics.reviews[0].keywords[1]="Pathétique";
	data.critics.reviews[1]=new Object;
	data.critics.reviews[1].journal="Le Monde";
	data.critics.reviews[1].grade=0.4;
	data.critics.reviews[1].keywords=new Array;
	data.critics.reviews[1].keywords[0]="Sérieux";
	data.critics.reviews[1].keywords[1]="Appliqué";
	data.critics.reviews[2]=new Object;
	data.critics.reviews[2].journal="Télé 7-Jours";
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
	data.bag_of_words[9].value=0.5;
	
	fctCallbackPredict(data);
		
}

function fctCallbackPredict(data){
	alert(JSON.stringify(data))
	//arreter=true;document.getElementById("loaderProvisoire").parentNode.removeChild(document.getElementById("loaderProvisoire"));montrerResultats("cadreProches");carrousel("cadreCoverflow");
}


