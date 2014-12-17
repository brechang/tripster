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

declare function local:getAuthUsers()
as element()*
{
    for $x in doc($docname)/tripster/user
    return
        <tuple>
            <ID>{data($x/id)}</ID>
            <PASSWORD>a</PASSWORD>
            <LAST_LOGIN>2014-12-05 03:27:08.983187</LAST_LOGIN>
            <IS_SUPERUSER>0</IS_SUPERUSER>
            <USERNAME>{data($x/login)}</USERNAME>
            <IS_STAFF>0</IS_STAFF>
            <IS_ACTIVE>1</IS_ACTIVE>
            <DATE_JOINED>2014-12-05 03:27:08.983187</DATE_JOINED>
        </tuple>
};

declare function local:getUsers()
as element()*
{
    for $x in doc($docname)/tripster/user
    return
        <tuple>
            <ID>{data($x/id)}</ID>
            <AFFILIATION>{data($x/affiliation)}</AFFILIATION>
            <USER_ID>{data($x/id)}</USER_ID>
            <AGE>0</AGE>
            <GENDER>None</GENDER>
            <URL>http://www.example.com</URL>
            <PRIVACY>1</PRIVACY>
        </tuple>
};

declare function local:getAlbum()
as element()*
{
    for $x in doc($docname)/tripster/user/trip
    for $y in $x/album
    return 
        <tuple>
            <ID>{data($y/id)}</ID>
            <NAME>{data($y/name)}</NAME>
            <TRIP_ID>{data($x/id)}</TRIP_ID>
            <TIMESTAMP>2014-12-05 03:27:08.983187</TIMESTAMP>
            <PRIVACY>1</PRIVACY>
        </tuple>
};

declare function local:getFriendID($name as xs:string)
as element()*
{
    for $x in doc($docname)/tripster/user
    where data($x/login) = $name  
    return $x/id
};

declare function local:getFriends()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/friend
    return
        if (empty(local:getFriendID(data($y))))
            then ()
        else
            <tuple> 
                <ID>{data($x/id) * 31 + data(local:getFriendID(data($y)))}</ID>
                <FROM_TRIPSTERUSER_ID>{data($x/id)}</FROM_TRIPSTERUSER_ID>
                <TO_TRIPSTERUSER_ID>{data(local:getFriendID(data($y)))}</TO_TRIPSTERUSER_ID>
            </tuple>
};

declare function local:getParticipants()
as element()*
{
    for $x in doc($docname)/tripster/user
        for $y in $x/trip
    return 
        <tuple>
            <ID>{data($y/id)}</ID>
            <TRIP_ID>{data($y/id)}</TRIP_ID>            
            <USER_ID>{data($x/id)}</USER_ID>            
        </tuple>
};

declare function local:getTripRating()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/rateTrip
    return
        <tuple>
        <ID>{data($y/id)}</ID>
        <RATING>{data($y/score)}</RATING>
        <TRIP_ID>{data($y/tripid)}</TRIP_ID>
        <USER_ID>{$x/id}</USER_ID>
        </tuple>
};

(: BRENDA SPACE :)
(: BRENDA: getContent, getContentOf, getContentComments, getContentCommentsOf :)

declare function local:getContent()
as element()*
{
   for $x in doc($docname)/tripster/user/trip/album
   for $y in $x/content
   return
       <tuple>
            <ID>{data($y/id)}</ID>
            <NAME>{data($y/type)}</NAME>
            <URL>{data($y/url)}</URL>
            <ALBUM_ID>{data($x/id)}</ALBUM_ID>
            <TIMESTAMP>2014-12-05 03:27:08.983187</TIMESTAMP>
            <PRIVACY>1</PRIVACY>
       </tuple>
};

declare function local:getContentComments()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/rateContent
    return
        <tuple>
            <ID>{data($y/id)}</ID>
            <CONTENT_ID>{data($y/contentid)}</CONTENT_ID>
            <COMMENT>{data($y/comment)}</COMMENT>
            <USER_ID>{data($x/id)}</USER_ID>
            <TIMESTAMP>2014-12-05 03:27:08.983187</TIMESTAMP>
        </tuple>
};

declare function local:getContentRating()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/rateContent
    return
        <tuple>
            <ID>{data($y/id)}</ID>
            <CONTENT_ID>{data($y/contentid)}</CONTENT_ID>
            <RATING>{data($y/score)}</RATING>
            <USER_ID>{data($x/id)}</USER_ID>
            <TIMESTAMP>2014-12-05 03:27:08.983187</TIMESTAMP>
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
        <NAME>blah</NAME>
        <TIMESTAMP>2014-12-05 03:27:08.983187</TIMESTAMP>
        <PRIVACY>1</PRIVACY>
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

declare function local:getTripLocation()
as element()*
{
    for $x in doc($docname)/tripster/user/trip
    for $y in $x/location
    return
        <tuple>
        <ID>{data($y/id)}</ID>
        <TRIP_ID>{data($x/id)}</TRIP_ID>
        <LOCATION_ID>{data($y/id)}</LOCATION_ID>
        </tuple>
};

declare function local:getTripComment()
as element()*
{
    for $x in doc($docname)/tripster/user
    for $y in $x/rateTrip
    return
        <tuple>
        <ID>{data($y/id)}</ID>
        <COMMENT>{data($y/score)}</COMMENT>
        <TRIP_ID>{data($y/tripid)}</TRIP_ID>
        <USER_ID>{$x/id}</USER_ID>
        <TIMESTAMP>2014-12-05 03:27:08.983187</TIMESTAMP>
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
    <AUTH_USERS>{local:getAuthUsers()}</AUTH_USERS>
    <TRIPSTER_TRIPSTERUSER>{local:getUsers()}</TRIPSTER_TRIPSTERUSER>
    <TRIPSTER_LOCATION>{local:getLocation()}</TRIPSTER_LOCATION>
    <TRIPSTER_TRIP>{local:getTrip()}</TRIPSTER_TRIP>
    <TRIPSTER_TRIP_LOCATIONS>{local:getTripLocation()}</TRIPSTER_TRIP_LOCATIONS>
    <TRIPSTER_TRIP_PARTICIPANTS>{local:getParticipants()}</TRIPSTER_TRIP_PARTICIPANTS>
    <TRIPSTER_TRIPSTERUSER_FRIENDS>{local:getFriends()}</TRIPSTER_TRIPSTERUSER_FRIENDS>
    <TRIPSTER_ALBUM>{local:getAlbum()}</TRIPSTER_ALBUM>
    <TRIPSTER_TRIPRATING>{local:getTripRating()}</TRIPSTER_TRIPRATING>
    <TRIPSTER_TRIPCOMMENT>{local:getTripComment()}</TRIPSTER_TRIPCOMMENT>
    <TRIPSTER_CONTENT>{local:getContent()}</TRIPSTER_CONTENT>
    <TRIPSTER_CONTENTCOMMENT>{local:getContentComments()}</TRIPSTER_CONTENTCOMMENT>
    <TRIPSTER_CONTENTRATING>{local:getContentRating()}</TRIPSTER_CONTENTRATING>
</database>
