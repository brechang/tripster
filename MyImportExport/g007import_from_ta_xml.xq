xquery version "3.0";

(:~
: User: haolinlu, brechang, fanyin
: Date: 11/16/14
: Time: 7:14 PM
: To change this template use File | Settings | File Templates.
:)



declare variable $docname := "ta_tripster.xml";

declare updating function local:insertIds($el)
{
    for $x at $pos in $el
    return (
        insert node <id>{$pos}</id> as first into $x
    )
};

declare updating function local:replaceIds($el)
{
    for $x at $pos in $el
    return (
        replace node $x/id with <id>{$pos}</id>
    )
};

(: KEVIN SPACE :)
(: KEVIN: getUsers, getAlbum, getAlbumOf, getFriendsWith, getParticipantsOf :)

declare function local:getUsername($id as xs:integer)
as xs:string?
{
    for $x in doc($docname)/database/USERS/tuple
    where data($x/ID) = $id
    return data($x/USERNAME)
};

declare function local:getAffiliation($id as xs:integer)
as xs:string?
{
    for $x in doc($docname)/database/USERS/tuple
    where data($x/ID) = $id
    return data($x/AFFILIATION)
};

declare function local:getFriends($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/FRIENDS_WITH/tuple
    where data($x/USER_ID) = $id
    return <friend> {local:getUsername(data($x/FRIEND_ID))} </friend>
};

declare function local:getFriendsId($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/FRIENDS_WITH/tuple
    where data($x/USER_ID) = $id
    return <friendid> {local:getUsername(data($x/FRIEND_ID))} </friendid>
};

declare function local:getContentURL($id as xs:integer)
{
    for $x in doc($docname)/database/CONTENT/tuple
    where data($x/ID) = $id
    return data($x/URL)
};


(: BRENDA SPACE :)
(: BRENDA: getContent, getContentOf, getContentComments, getContentCommentsOf :)

declare function local:getContent($id as xs:integer)
as element()*
{
   for $x in doc($docname)/database/CONTENT_OF/tuple
   where data($x/ALBUM_ID) = $id
   return
   <content>
        <id> {data($x/CONTENT_ID)} </id>
        <group> group1 </group>
        <type> photo </type>
        <url> {local:getContentURL($x/CONTENT_ID)}</url>
   </content>
};

declare function local:getAlbumName($id as xs:integer)
as xs:string
{
    for $x in doc($docname)/database/ALBUM/tuple
    where data($x/ID) = $id
    return data($x/NAME)
};

declare function local:getAlbum($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/ALBUM_OF/tuple
    where data($x/TRIP_ID) = $id
    return
        <album>
            <id> {data($x/ALBUM_ID)} </id>
            <name> {local:getAlbumName(data($x/ALBUM_ID))} </name>
            <privacyFlag> private </privacyFlag>
            {local:getContent(data($x/ALBUM_ID))}
        </album>
};

declare function local:getLocationName($id)
as xs:string
{
    for $x in doc($docname)/database/LOCATION/tuple
    where data($x/ID) = $id
    return data($x/NAME)
};

declare function local:getLocation($id)
as element()*
{
    for $x in doc($docname)/database/TRIP/tuple
    where data($x/USER_ID) = $id
    return <location> {local:getLocationName(data($x/LOCATION_ID))} </location>
};

(: FAN SPACE :)
(: FAN: getTrip, getTripComments, getTripCommentsOf, getLocation, getDreamLocation, getVisited :)

declare function local:getTrip()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/trip
    return 
        <tuple>
        <ID>{data($y/id)}</ID>
        <HOST_ID>{data($x/id)}</HOST_ID>
        <LOCATION_ID>{data{$y/location/id}}</LOCATION_ID>
        <RATING>0</RATING>
        </tuple>
};

declare function local:getLocation()
as element()*
{
    for $x in doc($docname)/tripster/user/trip/location
    return
        <tuple>
        <ID>{data($x/id)}</ID>
        <NAME>{data($x/name)}</NAME>
        </tuple>
};

declare function local:getTripComments()
as element()*
{
    for $x in doc($docname)/tripster/user/rateTrip
    return
        <tuple>
        <ID>{data($x/id)}</ID>
        <TRIP_ID>{data($x/tripid)}</TRIP_ID>
        <COMMENT_STR>{data($x/comment)}</COMMENT_STR>
        </tuple>
};

declare function local:getTripCommentsOf()
as element()*
{
    for $x in doc($docname)/tripster/user/rateTrip
    return
        <tuple>
        <TRIP_ID>{data($x/tripid)}</TRIP_ID>
        <COMMENT_ID>{data($x/id)}</COMMENT_ID>
        </tuple>
};

declare function local:getDreamLocation()
as element()*
{
    for $x in doc($docname)/tripster/user/dream
    return
        <tuple>
        <USER_ID>{data($x/id)}</USER_ID>
        <LOCATION_ID>1</LOCATION_ID>
        </tuple>
}

(: LP SPACE :)

declare variable $base := doc($docname)/tripster/user;

local:insertIds($base);
local:insertIds($base/trip/location);
local:insertIds($base/rateTrip);
local:insertIds($base/rateContent);

local:replaceIds($base/trip);
local:replaceIds($base/trip/album);
local:replaceIds($base/trip/album/content);

<tripster>
{for $x in doc($docname)/tripster/user
    return 
        <user>
        <id>{data($x/id)}</id>
        <trip><id>{data($x/trip/id)}</id></trip>
        </user>}
</tripster>
