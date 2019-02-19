% include('templates/header.tpl')
<div id="first">
    <div class="image">
    % if item['wiki_link']:
        <a href="{{ item['wiki_link'] }}" target="_blank">
    % else:
        <a href="#" target="_blank">
    % end
            <img src="/img/{{ item['imageName'] }}" alt="{{item['name']}}" width="100%"/>
        </a>
    </div>
    <div class="info">
    % if item['wiki_link']:
        <a href="{{ item['wiki_link'] }}" target="_blank">wiki</a> <br />
    % end
    % if item['market_link']:
        <a href="{{ item['market_link'] }}" target="_blank">market</a> <br />
    % end
        name: {{ item['name'] }} <br />

    </div>
    <div class="clear"></div>
</div>
<div id="drops">
    % if 'drops' in item:
        <table id="drop" class="sortable-table minimalistBlack">
            <thead>
                <tr>
                    <th>Place</th>
                    <th>Rarity</th>
                    <th class="numeric-sort">Chance</th>
                </tr>
            </thead>
            <tbody>
            % for drop in item['drops']:
                <tr class="item">
                    <td><a href="/place/{{!drop['link_place']}}">{{!drop['place'] }}</a></td>
                    <td>{{!drop['rarity']}}</td>
                    <td>{{!drop['chance']}}%</td>
                </tr>
            % end
            </tbody>
        </table>
    % end
    % if 'drops' not in item:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')