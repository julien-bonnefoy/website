window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        geojson_filter: function(feature, context) {return context.hideout.includes(feature.properties.uga);},
        uga_geojson_filter: function(feature, context) {{return context.hideout.selected.includes(feature.properties.CODE_UGA);}},
        cible_icon: function(feature, latlng) {
            const doctor_colors = {
                'GY': 'pink',
                'MG-GY': 'pink',
                'SF': 'pink',
                'MG': '#aaa',
                'GE': 'orange',
                'PE': 'cyan',
                'PE-PSY': 'blue-dark',
                'PSY': 'purple',
                'NE': 'violet',
            };
            const marker = L.ExtraMarkers.icon({
                icon: 'fa-user-doctor',
                prefix: 'fa',
                markerColor: doctor_colors[feature.properties.spe],
                iconColor: 'white',
                shape: 'square',
                svg: true
            });
            return L.marker(latlng, {
                icon: marker
            });
        },
        pharma_icon: function(feature, latlng) {
            const pmarker = L.ExtraMarkers.icon({
                icon: 'fa-prescription-bottle-medical',
                prefix: 'fa',
                markerColor: 'green',
                iconColor: doctor_colors[feature.properties.spe],
                shape: 'circle',
            });
            return L.marker(latlng, {
                icon: pmarker
            });
        },
        uga_style_handle: function(feature, context){
            const {selected} = context.hideout;
            if(selected.includes(feature.properties.CODE_UGA)){
                return {fillColor: 'red', color: 'grey'}
            }
            return {fillColor: 'grey', color: 'grey'}
        }
    }
});