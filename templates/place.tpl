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
            <div class="text_level">{{!level}}</div>
            <div class="place_level grid-container grid-container--fill">
                % for rotation in sorted(place['levels'][level]['drops']):
                    % if len(place['levels'][level]['drops'][rotation]) == 0:
                        % continue
                    % end

                    <div class="drop_place">
                        % if rotation != 'normal':
                            <div class="text_rotation">Rotation {{!rotation}}</div>
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
                                    <td><a href="/item/{{!drop['item']}}">{{!drop['item'] }}</a></td>
                                    <td>{{!drop['rarity'] }}</td>
                                    <td>{{!drop['chance'] }}%</td>
                                </tr>
                            % end
                            </tbody>
                        </table>
                    </div>
                % end
                <div class="clear"></div>
            </div>
        % end
    % else:
        info not available
    % end
    <div class="clear"></div>
</div>

% include('templates/footer.tpl')