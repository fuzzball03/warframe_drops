% include('templates/header.tpl')
<div id="first">
    <div class="info">
        name: {{ place['name'] }} <br />
    </div>
    <div class="clear"></div>
</div>
<div id="drops">
    % if 'drops' in place:
        % for rotation in place['drops']:
            % if len(place['drops'][rotation]) == 0:
                % continue
            % end
            % if rotation == 'normal':
                Always
            % else:
                Rotation {{!rotation}}
            % end

            <table id="drop" class="sortable-table minimalistBlack">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Rarity</th>
                        <th class="numeric-sort">Chance</th>
                    </tr>
                </thead>
                <tbody>

                %for drop in place['drops'][rotation]:
                    <tr class="item">
                        <td>{{!drop['item'] }}</td>
                        <td>{{!drop['rarity'] }}</td>
                        <td>{{!drop['chance'] }}%</td>
                    </tr>
                % end
                </tbody>
            </table>
        % end
    % end
    % if 'drops' not in place:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')