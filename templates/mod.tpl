% include('templates/header.tpl')
<div id="first">
    <div class="image">
        <a href="{{ mod['wiki_link'] }}" target="_blank">
            <img src="/img/{{ mod['imageName'] }}" width="100%"/>
        </a>
    </div>
    <div class="info">
        <a href="{{ mod['wiki_link'] }}" target="_blank">wiki</a> <br />
        <a href="{{ mod['market_link'] }}" target="_blank">market</a> <br />
        name: {{ mod['name'] }} <br />
        <!-- description: {{ mod['description'] }} <br /> -->
        rarity: {{ mod['rarity'] }} <br />
        baseDrain: {{ mod['baseDrain'] }} <br />
        fusionLimit: {{ mod['fusionLimit'] }} <br />
        tradable: {{ mod['tradable'] }} <br />
        type: {{ mod['type'] }} <br />
        <!-- category: {{ mod['category'] }} <br /> -->
        polarity: {{ mod['polarity'] }} <br />
    </div>
    <div class="clear"></div>
</div>
<div id="drops">
    % if 'drops' in mod:
        <table id="drop" class="minimalistBlack">
            <tr>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(1)')">Location</th>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(2)')">Type</th>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(3)')">Rarity</th>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(4)')">Change</th>
            </tr>
            % for drop in mod['drops']:
                <tr class="item">
                    <td>{{ drop['location'] }}</td>
                    <td>{{ drop['type'] }}</td>
                    <td>{{ drop['rarity'] }}</td>
                    <td>{{ drop['chance'] }}%</td>
                </tr>
            % end
        </table>
    % end
    % if 'drops' not in mod:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')