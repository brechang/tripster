xquery version "3.0";

(:~
: User: luhkevin
: Date: 11/16/14
: Time: 7:14 PM
: To change this template use File | Settings | File Templates.
:)

declare function local:getUsername($id as xs:integer)
as xs:string?
{
    for $x in doc("export.xml")/database/USERS/tuple
    where data($x/ID) = $id
    return data($x/USERNAME)
};

declare function local:getAffiliation($id as xs:integer)
as xs:string?
{
    for $x in doc("export.xml")/database/USERS/tuple
    where data($x/ID) = $id
    return data($x/AFFILIATION)
};

declare function local:getFriends($id as xs:integer)
as element()*
{
    for $x in doc("export.xml")/database/FRIENDS_WITH/tuple
    where data($x/USER_ID) = $id
    return <friend> {local:getUsername(data($x/FRIEND_ID))} </friend>
};

declare function local:getFriendsId($id as xs:integer)
as element()*
{
    for $x in doc("export.xml")/database/FRIENDS_WITH/tuple
    where data($x/USER_ID) = $id
    return <friendid> {local:getUsername(data($x/FRIEND_ID))} </friendid>
};

declare function local:getContentURL($id as xs:integer)
{
    for $x in doc("export.xml")/database/CONTENT/tuple
    where data($x/ID) = $id
    return data($x/URL)
};

declare function local:getContent($id as xs:integer)
as element()*
{
   for $x in doc("export.xml")/database/CONTENT_OF/tuple
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
    for $x in doc("export.xml")/database/ALBUM/tuple
    where data($x/ID) = $id
    return data($x/NAME)
};

declare function local:getAlbum($id as xs:integer)
as element()*
{
    for $x in doc("export.xml")/database/ALBUM_OF/tuple
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
    for $x in doc("export.xml")/database/LOCATION/tuple
    where data($x/ID) = $id
    return data($x/NAME)
};

declare function local:getLocation($id)
as element()*
{
    for $x in doc("export.xml")/database/TRIP/tuple
    where data($x/USER_ID) = $id
    return <location> {local:getLocationName(data($x/LOCATION_ID))} </location>
};

declare function local:getTrip($id as xs:integer)
as element()*
{
    for $x in doc("export.xml")/database/PARTICIPANTS_OF/tuple
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
    for $x in doc("export.xml")/database/PARTICIPANTS_OF/tuple
    where data($x/USER_ID) = $id
    return
        <rateTrip>
            <id> {data($x/TRIP_ID)} </id>
            <score> foo name </score>
            {local:getTripComments($x/TRIP_ID)}
        </rateTrip>
};

declare function local:getTripComments($id as xs:integer)
as element()*
{
    for $x in doc("export.xml")/database/TRIP_COMMENTS/tuple
    where data($x/TRIP_ID) = $id
    return
        <comments>{data($x/COMMENT_STR)}</comments>
};

<tripster xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ta_tripster.xsd">
<User>
    <login> {local:getUsername(1)} </login>
    <email> {local:getUsername(1)}@example.com </email>
    <name> {local:getUsername(1)} </name>
    <affiliation> {local:getAffiliation(1)} </affiliation>
    <interests> Surfing </interests>
    {local:getFriends(1)}
    {local:getTrip(1)}

    {local:getUserTripRating(1)}

    <rateContent>
    </rateContent>

    <request>
        <tripid> 3 </tripid>
        <status> pending </status>
    </request>

    <invite>
        <tripid> 1 </tripid>
        {local:getFriendsId(1)}
        <status> pending </status>
    </invite>
</User>

<User>
    {local:getUsername(2)}
</User>
</tripster>
