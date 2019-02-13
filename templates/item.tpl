% include('templates/header.tpl')
<div id="first">
    <div class="image">
        <a href="{{ item['wiki_link'] }}" target="_blank">
            <img src="/img/{{ item['imageName'] }}" width="100%"/>
        </a>
    </div>
    <div class="info">
        <a href="{{ item['wiki_link'] }}" target="_blank">wiki</a> <br />
        <a href="{{ item['market_link'] }}" target="_blank">market</a> <br />
        name: {{ item['name'] }} <br />

    </div>
    <div class="clear"></div>
</div>
<div id="drops">
    % if 'drops' in item:
        <table id="drop" class="minimalistBlack">
            <tr>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(1)')">Place</th>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(2)')">Rarity</th>
                <th onclick="w3.sortHTML('#drop', '.item', 'td:nth-child(3)')">Chance</th>
            </tr>
            % for drop in item['drops']:
                <tr class="item">
                    <td>{{!drop['place'] }}</td>
                    <td>{{!drop['rarity'] }}</td>
                    <td>{{!drop['chance'] }}%</td>
                </tr>
            % end
        </table>
    % end
    % if 'drops' not in item:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')