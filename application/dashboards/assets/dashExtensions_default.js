window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        geojson_filter: function(feature, context) {return context.hideout.selected.includes(feature.properties.uga);},
        uga_geojson_filter: function(feature, context) {return context.hideout.selected.includes(feature.properties.CODE_UGA);},
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
            if (feature.properties.ciblage>0) {
                var iconColor = 'white'
                var shape = 'star'
            } else {
                var iconColor = 'red'
                var shape = 'square'
            };
            const marker = L.ExtraMarkers.icon({
                icon: 'fa-user-doctor',
                prefix: 'fa',
                markerColor: doctor_colors[feature.properties.spe],
                iconColor: iconColor,
                shape: shape,
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
                iconColor: 'white',
                shape: 'circle',
            });
            return L.marker(latlng, {
                icon: pmarker
            });
        },
        uga_style_handle: function(feature, context){
            const uga_colors = {
                '75AUT': '#ff0000',
                '75PAS': '#bd0071',
                '75TRO': '#410E66',
                '75INV': '#130066',
                '75ELY': '#fe7600',
                '75GRE': '#060087',
                '75VAU': '#00877d',
                '75MNP': '#008000',
                '75PER': '#32cd32',
                '75TER': '#00fa9a',
                '92LEV': '#adff2f',
                '92NEU': '#f3ff00'
            };
            return {opacity: 1, dashArray: '5', fillOpacity: 0.1, weight:1, fillColor: uga_colors[feature.properties.CODE_UGA], color: uga_colors[feature.properties.CODE_UGA]}
        }
    }
});