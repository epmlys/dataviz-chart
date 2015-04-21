define([
  'jquery',
  'underscore',
  'backbone',
  'models/builds_status',
  'models/time_durations'
], function (
    $,
    _,
    Backbone,
    BuildsStatusModel,
    TimeDurationsModel
) {

  return Backbone.View.extend({

    initialize: function (options) {
        _.bindAll(
            this,
            'getAbnormalThreshold'
        );
	this.statusModel = new BuildsStatusModel();
	this.durationsModel = new TimeDurationsModel();
    },

    getAbnormalThreshold: function (numsFailed) {
        var sorted = _.without(numsFailed, 0).sort();
        // median
        var half = Math.floor(sorted.length/2);
        if (sorted.length % 2) {
           return sorted[half]
        } else {
           return(sorted[half-1] + sorted[half]) / 2
        }
    },

    render: function () {
	this.statusModel.fetch().done(
            _.bind(function (data) {
                var numsPassed = _.pluck(_.values(data), 'passed'),
                    numsFailed = _.pluck(_.values(data), 'failed'),
                    abnormalThreshold = this.getAbnormalThreshold(numsFailed);
                $('#statusChartContainer').highcharts({
    		    chart: {
        	    type: 'column'
    		    },
    		    title: {
        		text: 'Passed and Failed builds'
    		    },
    		    xAxis: {
        		categories: _.keys(data),
    		    },
    		    yAxis: {
        		min: 0,
        		title: {
            		    text: 'Total builds per day'
        		},
        		stackLabels: {
            		    enabled: true,
            		    style: {
                		fontWeight: 'bold',
                		color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
            		    }
        		}
    		    },
    		    legend: {
        		align: 'right',
        		x: -30,
        		verticalAlign: 'top',
        		y: 25,
        		floating: true,
        		backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
        		borderColor: '#CCC',
        		borderWidth: 1,
        		shadow: false
    		    },
    		    tooltip: {
        		formatter: function () {
            		    return '<b>' + this.x + '</b><br/>' +
                	    this.series.name + ': ' + this.y + '<br/>' +
                	    'Total: ' + this.point.stackTotal;
        		}
    		    },
    		    plotOptions: {
        		column: {
            		    stacking: 'normal',
            		    dataLabels: {
                		enabled: true,
                		color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                		style: {
                    		textShadow: '0 0 3px black'
                		}
            		    }
        		}
    		    },
    		    series: [{
        	    name: 'Passed',
        	    data: numsPassed
    		    }, {
        	    name: 'Failed',
        	    data: _.map(numsFailed, function (val) {
                                var res = val > abnormalThreshold ? {color: '#FF0000', y: val} : val;
                                return res;})
    		    }]
		});

                }, this)
            ).fail(_.bind(function (data) {
		this.$el.find('#buildsChartContainer').html(
		    'Sorry, can not load Builds History Chart.');
            }, this));
	
	this.durationsModel.fetch().done(_.bind(function (data) {
	    $('#durationChartContainer').highcharts({
        title: {
            text: 'Time vs Duration over day'
        },
        xAxis: {
            categories: _.keys(data)
        },
        yAxis: {
            title: {
                text: 'Duration (sec.)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: 's'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'All builds',
            data: _.values(data)
        }]
	});

	    }, this));
    }

  });
});
