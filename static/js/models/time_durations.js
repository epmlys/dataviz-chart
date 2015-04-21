define([
    'underscore',
    'backbone'
], function (
    _,
    Backbone
) {

    var BASE_URL = '/durations';

    return Backbone.Model.extend({
        url: function () {
            return BASE_URL;
        },

        initialize: function () {
            _.bindAll(
                this
            );
        },

        parse: function(response){
            return {'data': response};
        }
    });
});
