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

declare function local:getUsers()
as element()*
{
    for $x in doc($docname)/tripster
    for $y in $x/user

    return
        <tuple>
            <ID>data($y/id)</ID>
            <USERNAME>data($y/login)</USERNAME>
            <ENC_PWORD>data($y/password)</ENC_PWORD>
            <AFFILIATION>data($y/affiliation)</AFFILIATION>
        </tuple>
};

declare function local:getAlbum()
as element()*
{
    for $x in doc($docname)/tripster/user/trip
    for $y in $x/album
    return 
        <tuple>
            <ID>data($y/id)</ID>
            <NAME>data($y/name)</NAME>
        </tuple>
};


declare function local:getAlbumOf()
as element()*
{
    for $x in doc($docname)/tripster/user/trip
    for $y in $x/album
    return 
        <tuple>
            <ALBUM_ID>data($y/id)</ALBUM_ID>
            <TRIP_ID>data($x/id)</TRIP_ID>
        </tuple>
};

declare function local:getFriendID($name as xs:string)
as xs:integer
{
    for $x in doc($docname)/tripster
        for $y in $x/user
           where ($x/name) = $name  
        return data($y/id)
}

declare function local:getFriendsWith()
as element()*
{
    for $x in doc($docname)/tripster
        for $y in $x/user
    return 
        <tuple> 
            <USER_ID>data($y/id)</USER_ID>
            <FRIEND_ID>{local:getFriendID(data($y/name))}</FRIEND_ID>
        </tuple>
};

declare function local:getParticipantsOf()
as element()*
{
    for $x in doc($docname)/tripster
        for $y in $x/trip
    return 
        <tuple>
            <TRIP_ID>data($y/id)</TRIP_ID>            
            <USER_ID>data($x/user/id)</USER_ID>            
        </tuple>
};

(: BRENDA SPACE :)
(: BRENDA: getContent, getContentOf, getContentComments, getContentCommentsOf :)

declare function local:getContent()
as element()*
{
   for $x in doc($docname)/tripster/user/trip/album/content
   return
       <tuple>
            <ID>{data($x/id)}</ID>
            <RATING>0</RATING>
            <NAME>{data($x/type)}</NAME>
            <URL>{data($x/url)}</URL>
       </tuple>
};

declare function local:getContentOf()
as element()*
{
    for $x in doc($docname)/tripster/user/trip/album
    for $y in $x/content
    return
        <tuple>
            <ALBUM_ID>{data($x/id)}</ALBUM_ID>
            <CONTENT_ID>{data($y/id)}</CONTENT_ID>
        </tuple>
};

declare function local:getContentComments()
as element()*
{
    for $x in doc($docname)/tripster/user/rateContent
    return
        <tuple>
            <ID>{data($x/id)}</ID>
            <CONTENT_ID>{data($x/contentid)}</CONTENT_ID>
            <COMMENT_STR>{data($x/comment)}</COMMENT_STR>
        </tuple>
};

declare function local:getContentCommentsOf()
as element()*
{
    for $x in doc($docname)/tripster/user/rateContent
    return
        <tuple>
            <CONTENT_ID>{data($x/contentid)}</CONTENT_ID>
            <COMMENT_ID>{data($x/id)}</COMMENT_ID>
        </tuple>
};

(: FAN SPACE :)
(: FAN: getTrip, getTripComments, getTripCommentsOf, getLocation, getDreamLocation, getVisited :)

declare function local:getTrip($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return
        <trip>
            <id> {data($x/TRIP_ID)} </id>
            <name> foo name </name>
            <feature> foo feature </feature>
            <privacyFlag> private </privacyFlag>
            {local:getAlbum($x/TRIP_ID)}
            {local:getLocation($x/TRIP_ID)}
        </trip>
};

declare function local:getUserTripRating($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return
        <rateTrip>
            <id> {data($x/TRIP_ID)} </id>
            {local:getTripScore($x/TRIP_ID)}
            {local:getTripComments($x/TRIP_ID)}
        </rateTrip>
};

declare function local:getTripComments($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/TRIP_COMMENTS/tuple
    where data($x/TRIP_ID) = $id
    return <comments>{data($x/COMMENT_STR)}</comments>
};

declare function local:getTripScore($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/TRIP/tuple
    where data($x/ID) = $id
    return
        <score>{data($x/RATING)}</score>
};

declare function local:getUserTripID($id as xs:integer)
as xs:integer
{
    for $x in doc($docname)/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return data($x/TRIP_ID)
};

declare function local:getUserTripAlbum($id as xs:integer)
as xs:integer
{
  for $x in doc($docname)/database/ALBUM_OF/tuple
  where data($x/TRIP_ID) = $id
  return data($x/ALBUM_ID)
};

declare function local:getUserAlbumContent($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/CONTENT_OF/tuple
    where data($x/ALBUM_ID) = $id
    return $x
};

declare function local:getUserContentRating($id as xs:integer)
as element()*
{
    for $x in local:getUserAlbumContent(local:getUserTripAlbum(local:getUserTripID($id)))
        (: doc($docname)/database/CONTENT/tuple :)
    (: where data($x/ID) = local:getUserAlbumContent(local:getUserTripAlbum(local:getUserTripID($id))) :)

    return
        <rateContent>
            <contentid>{data($x/CONTENT_ID)}</contentid>
            <contentSource>group1</contentSource>
            <score>{data($x/RATING)}</score>
            {local:getContentComment(data($x/CONTENT_ID))}
        </rateContent>
};

declare function local:getContentComment($id as xs:integer)
as element()*
{
    for $x in doc($docname)/database/CONTENT_COMMENTS/tuple
    where data($x/CONTENT_ID) = $id
    return
        <comment>{data($x/COMMENT_STR)}</comment>

};

declare function local:getTripsterData() as
element()*
{
for $x in doc($docname)/database/USERS/tuple/ID
return
<User>
    <login> {local:getUsername($x)} </login>
    <email> {local:getUsername($x)}@example.com </email>
    <name> {local:getUsername($x)} </name>
    <affiliation> {local:getAffiliation($x)} </affiliation>
    <interests> Surfing </interests>
    {local:getFriends($x)}
    {local:getTrip($x)}
    {local:getUserTripRating($x)}
    {local:getUserContentRating($x)}

    <request>
        <tripid> 3 </tripid>
        <status> pending </status>
    </request>

    <invite>
        <tripid> 1 </tripid>
        {local:getFriendsId($x)}
        <status> pending </status>
    </invite>
</User>
};

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
