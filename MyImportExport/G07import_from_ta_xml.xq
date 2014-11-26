xquery version "3.0";

(:~
: User: haolinlu, brechang, fanyin
: Date: 11/16/14
: Time: 7:14 PM
: To change this template use File | Settings | File Templates.
:)

declare variable $docname := "project_data.xml";

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
    for $x in doc($docname)/tripster/user
    return
        <tuple>
            <ID>{data($x/id)}</ID>
            <USERNAME>{data($x/login)}</USERNAME>
            <ENC_PWORD>{data($x/password)}</ENC_PWORD>
            <AFFILIATION>{data($x/affiliation)}</AFFILIATION>
        </tuple>
};

declare function local:getAlbum()
as element()*
{
    for $x in doc($docname)/tripster/user/trip/album
    return 
        <tuple>
            <ID>{data($x/id)}</ID>
            <NAME>{data($x/name)}</NAME>
        </tuple>
};


declare function local:getAlbumOf()
as element()*
{
    for $x in doc($docname)/tripster/user/trip
    for $y in $x/album
    return 
        <tuple>
            <ALBUM_ID>{data($y/id)}</ALBUM_ID>
            <TRIP_ID>{data($x/id)}</TRIP_ID>
        </tuple>
};

declare function local:getFriendID($name as xs:string)
as element()*
{
    for $x in doc($docname)/tripster/user
    where data($x/login) = $name  
    return 
        <FRIEND_ID>{data($x/id)}</FRIEND_ID>
};

declare function local:getFriendsWith()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/friend
    return 
        <tuple> 
            <USER_ID>{data($x/id)}</USER_ID>
            {local:getFriendID(data($y))}
        </tuple>
};

declare function local:getParticipantsOf()
as element()*
{
    for $x in doc($docname)/tripster/user
        for $y in $x/trip
    return 
        <tuple>
            <TRIP_ID>{data($y/id)}</TRIP_ID>            
            <USER_ID>{data($x/id)}</USER_ID>            
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

declare function local:getTrip()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/trip
    return 
        <tuple>
        <ID>{data($y/id)}</ID>
        <HOST_ID>{data($x/id)}</HOST_ID>
        <LOCATION_ID>{data($y/location/id)}</LOCATION_ID>
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
    for $x in doc($docname)/tripster/user
    return
        <tuple>
        <USER_ID>{data($x/id)}</USER_ID>
        <LOCATION_ID>1</LOCATION_ID>
        </tuple>
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

<database>
    <USERS>{local:getUsers()}</USERS>
    <TRIP>{local:getTrip()}</TRIP>
    <LOCATION>{local:getLocation()}</LOCATION>
    <ALBUM>{local:getAlbum()}</ALBUM>
    <ALBUM_OF>{local:getAlbumOf()}</ALBUM_OF>
    <CONTENT>{local:getContent()}</CONTENT>
    <CONTENT_OF>{local:getContentOf()}</CONTENT_OF>
    <DREAM_LOCATION_OF>{local:getDreamLocation()}</DREAM_LOCATION_OF>
    <VISITED></VISITED>
    <PARTICIPANTS_OF>{local:getParticipantsOf()}</PARTICIPANTS_OF>
    <TRIP_COMMENTS>{local:getTripComments()}</TRIP_COMMENTS>
    <TRIP_COMMENTS_OF>{local:getTripCommentsOf()}</TRIP_COMMENTS_OF>
    <FRIENDS_WITH>{local:getFriendsWith()}</FRIENDS_WITH>
    <CONTENT_COMMENTS>{local:getContentComments()}</CONTENT_COMMENTS>
    <CONTENT_COMMENTS_OF>{local:getContentCommentsOf()}</CONTENT_COMMENTS_OF>
</database>
