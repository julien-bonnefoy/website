window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        geojson_filter: function(feature, context) {return context.hideout.ugas_selected.includes(feature.properties.uga) && context.hideout.spes_selected.includes(feature.properties.spe1) && context.hideout.cib_selected.includes(feature.properties.c24c1) && context.hideout.pvm_range[0]<feature.properties.pvm && context.hideout.pvm_range[1]>feature.properties.pvm;},
        pharmas_filter: function(feature, context) {return context.hideout.ugas_selected.includes(feature.properties.uga) && context.hideout.cib_selected.includes(feature.properties.c24c1);},
        uga_geojson_filter: function(feature, context) {return context.hideout.selected.includes(feature.properties.CODE_UGA);},
        cible_icon: function(feature, latlng) {
            const doctor_colors = {
                'GY': '#bd0071',
                'MGY': '#bd0071',
                'SF': '#bd0071',
                'MG': '#ffff46',
                'GE': '#fe7600',
                'PE': '#0080ff',
                'PPSY': '#410E66',
                'PSY': '#410E66',
                'NE': '#410e66',
                '': '#000000'
            };
            if (feature.properties.c24c1 > 0) {
                var shape = 'star'
            } else {
                var shape = 'square'
            };
            const marker = L.ExtraMarkers.icon({    
                icon: 'fa-user-doctor',
                prefix: 'fa',
                markerColor: doctor_colors[feature.properties.spe1],
                iconColor: 'white',
                shape: shape,
                svg: true
            })
            var m = L.marker(latlng, {
                icon: marker
            });
            var tooltip = L.tooltip(latlng, {direction: 'top', content: feature.properties.nom, offset: L.point(0, -40)});
            m.bindTooltip(tooltip)
            return m
        },
        pharmas_icon: function(feature, latlng) {
            console.log(feature)
            if (feature.properties.c24c1 > 0) {
                var shape = 'star'
            } else {
                var shape = 'square'
            };
            const pmarker = L.ExtraMarkers.icon({
                icon: 'fa-prescription-bottle-alt',
                prefix: 'fa',
                markerColor: 'green',
                iconColor: 'white',
                shape: shape,
                svg: true
            });
            var m = L.marker(latlng, {
                icon: pmarker
            });
            var tooltip = L.tooltip(latlng, {direction: 'top', content: feature.properties.nom, offset: L.point(0, -40)});
            m.bindTooltip(tooltip)
            return m
        },
        uga_style_handle: function(feature, context){
            const uga_colors = {
                '75AUT': '#164863',
                '75PAS': '#427D9D',
                '75TRO': '#9BBEC8',
                '75INV': '#1b7a02',
                '75ELY': '#A7D129',
                '75GRE': '#9A1663',
                '75VAU': '#E0144C',
                '75MNP': '#FF5858',
                '75PER': '#ec863d',
                '75TER': '#FE7600',
                '92LEV': '#994D1C',
                '92NEU': '#E48F45'
            };
            return {fillColor: uga_colors[feature.properties.CODE_UGA], fillOpacity: 0.3,  color: uga_colors[feature.properties.CODE_UGA], opacity: 1, weight:5, dashArray: '5'}
        },
    }
});