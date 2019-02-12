% include('templates/header.tpl')
<div id="first">
    <div class="image">
        <img src="/img/{{ mod['imageName'] }}" />
    </div>
    <div class="info">
        name: {{ mod['name'] }} <br />
        description: {{ mod['description'] }} <br />
        rarity: {{ mod['rarity'] }} <br />
        baseDrain: {{ mod['baseDrain'] }} <br />
        fusionLimit: {{ mod['fusionLimit'] }} <br />
        tradable: {{ mod['tradable'] }} <br />
        type: {{ mod['type'] }} <br />
        category: {{ mod['category'] }} <br />
        polarity: {{ mod['polarity'] }} <br />
    </div>
    <div class="clear"></div>
</div>
<div id="drops">
    % if 'drops' in mod:
        % for drop in mod['drops']:
        <div class="drop">
            location: {{ drop['location'] }}<br />
            rarity: {{ drop['rarity'] }}<br />
            type: {{ drop['type'] }}<br />
            chance: {{ drop['chance'] }}%<br />
        </div>
        % end
    % end
    % if 'drops' not in mod:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')