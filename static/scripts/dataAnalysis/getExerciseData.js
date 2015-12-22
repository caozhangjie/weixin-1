/**
 * Created by littlepig on 2015/11/30.
 */
$(document).ready(function(){
	$(function () {
		$('#collapseOne').collapse('show');
		$('#collapseTwo').collapse('show');
		$('#collapseThree').collapse('show');
		$('#collapseFour').collapse('show');
	});
	get_userinfo(function(data){
		openid = data.openid;
		nickname = data.nickname;
		headimgurl = data.headimgurl;
		headimgurl = data.headimgurl;
		$.getJSON("data/getsportsdata?openid="+openid, function(sportsData){
			renderByJson(sportsData);
		})
	});
})

function draw(){

	drawChart(getRandomArray(7), 7,"7-days-dis");
	drawChart(getRandomArray(7), 7, "7-days-steps");
	drawChart(getRandomArray(7), 7, "7-days-speed");
	drawChart(getRandomArray(7), 7, "7-days-calories");

	drawChart(getRandomArray(30), 30,"30-days-dis");
	drawChart(getRandomArray(30), 30, "30-days-steps");
	drawChart(getRandomArray(30), 30, "30-days-speed");
	drawChart(getRandomArray(30), 30, "30-days-calories");

	setDataText("7-days-dis-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("30-days-dis-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("7-days-steps-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("30-days-steps-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("7-days-speed-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("30-days-speed-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("7-days-calories-avg",  Math.floor(Math.random()*24)+1, "");
	setDataText("30-days-calories-avg",  Math.floor(Math.random()*24)+1, "");
}

//draw the charts and change the data according to the json
function renderByJson(json){
	if (json.isnull == true) {
		draw();
	}
	drawChart(json["7-days-dis"], 7,"7-days-dis");
	drawChart(json["7-days-steps"], 7, "7-days-steps");
	drawChart(json["7-days-speed"], 7, "7-days-speed");
	drawChart(json["7-days-calories"], 7, "7-days-calories");

	drawChart(json["30-days-dis"], 30,"30-days-dis");
	drawChart(json["30-days-dis"], 30, "30-days-steps");
	drawChart(json["30-days-dis"], 30, "30-days-speed");
	drawChart(json["30-days-dis"], 30, "30-days-calories");

	setDataText("7-days-dis-avg", json["7-days-dis-avg"], "");
	setDataText("30-days-dis-avg", json["30-days-dis-avg"], "");
	setDataText("7-days-steps-avg", json["7-days-steps-avg"], "");
	setDataText("30-days-steps-avg", json["30-days-steps-avg"], "");
	setDataText("7-days-speed-avg", json["7-days-speed-avg"], "");
	setDataText("30-days-speed-avg", json["30-days-speed-avg"], "");
	setDataText("7-days-calories-avg", json["7-days-calories-avg"], "");
	setDataText("30-days-calories-avg", json["30-days-calories-avg"], "");
}

//draw a chart
function drawChart(data, dataLength, chartId){
	var dataPointArray = []
    for (var i = 0; i < dataLength; i += 1) {
        dataPointArray.push([i,data[i]]);
    }
	$.plot($("#" + chartId),
		[ { data: dataPointArray}], {
			series: {
				lines: { show: true },
				points: { show: true }
			},

			grid: { hoverable: true, clickable: true },
			xaxis: { min: 0, max: dataLength - 1 },
		});
}

//set the advise
function setExpertiseAdvise(yesterdayIntensity, sevenDayIntensity){

}
//set data according to the data, "suffix" is the unit
function setDataText(idString, data, suffix){
	$("#" + idString).text(String(data) + suffix);
}
//test for random data
function getRandomArray(length){
	var data = [];
	for(var i = 0; i < length; i++){
		data.push(Math.floor(Math.random()*24)+1);
	}
	return data;
}