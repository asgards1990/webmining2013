
$(document).ready(function(){

critereEnable = false;
	function createClick(nom) {

		if (nom=="movieinput") {
        			
			$("#movieinput").keyup(function(event){
			if(event.keyCode == 13){
			var p = this.parentNode;
			var element = this.parentNode.parentNode;
			var value = this.value
			var textNode = document.createTextNode(value)
			p.removeChild(this);

			p.appendChild(textNode);
			element.getElementsByTagName("img")[0].src="http://goo.gl/8IrUDR";

			var deleteicon = document.createElement('div');
			deleteicon.className = "deleteicon";
			deleteicon.style="cursor: pointer;"; 

			var image = document.createElement('img');
			image.style="max-height:1.4em;max-width:1.4em";
			image.src="http://goo.gl/61lXjQ";
			image.alt="Edit";

			deleteicon.appendChild(image);
			element.appendChild(deleteicon);
			
			if (critereEnable==false) {
				var tabCriteres=document.getElementById("filters").getElementsByTagName("input");
				var formGenres=document.getElementById("genres").getElementsByTagName("form")[0];
				var formBudget=document.getElementById("slider-range");
				var formReviews=document.getElementById("ex_1b");
				
			
				critereEnable=true;
			
			for (k=0; k<tabCriteres.length;k++)   {
				tabCriteres[k].disabled=false; 
				formGenres.style.display = "block";
				formBudget.style.display = "block";
				formReviews.style.display = "block";
			
				}
			
			}
	createClick(deleteicon);
			}
		});
		

	}


		else {$(".deleteicon").click(function(){
			var p = this.parentNode.getElementsByTagName("p")[0];
			text = p.textContent;
			var element = this.parentNode;
			var movieinput = document.createElement('input');
			var newP = document.createElement('p');
			element.getElementsByTagName("img")[0].src="http://goo.gl/cO7yqA";


			element.removeChild(this);
			element.removeChild(p);


			movieinput.id="movieinput";
			movieinput.type="text";
			movieinput.name="actorname"
			movieinput.value=text;
			movieinput.size="12";
			movieinput.style="text-align : left";

			newP.appendChild(movieinput);
			element.appendChild(newP);
	
		createClick("movieinput");
			});	
		}
	};
	
createClick("movieinput");	
	
	

});

	



