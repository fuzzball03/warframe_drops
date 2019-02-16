% include('templates/header.tpl')
<div id="first">
    <div class="info">
        name: {{ place['name'] }} <br />
    </div>
    <div class="clear"></div>
</div>
<div id="drops">
    % if 'levels' in place:
        % for level in sorted(place['levels']):
            {{!level}}
            % for rotation in sorted(place['levels'][level]['drops']):
                % if len(place['levels'][level]['drops'][rotation]) == 0:
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

                    %for drop in place['levels'][level]['drops'][rotation]:
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
    % else:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')