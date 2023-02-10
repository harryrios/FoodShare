create schema foodshare_db;

use foodshare_db;

create table account(
    id          bigint not null,
    email       varchar(20) not null,
    password    varchar(40) not null,
    acc_type    varchar(10) not null,

    primary key(id),
    check(acc_type='manager'
              or acc_type='shopper')
);

create table pantry_shopper_pair(
    pantry_id     bigint not null,
    shopper_id    bigint not null,
    primary key(pantry_id, shopper_id),
    foreign key(pantry_id) references pantry(id),
    foreign key(shopper_id) references account(id)
);


create table pantry(
    id          bigint not null,
    inventory_id bigint not null,
    name    varchar(40) not null,
    manager_id  bigint not null,

    primary key(id),
    foreign key(inventory_id) references inventory(id),
    foreign key(manager_id) references account(id)
);
create table inventory(
    id          bigint not null,
    item_id     bigint not null,

    primary key(id),
    foreign key(item_id) references inventory_item(id)
);

create table generic_item(
    id          bigint not null,
    item_type   varchar(20) not null,
    primary key(id)
);
create table transaction(
    id          bigint not null,
    shopper_id  bigint not null,
    pantry_id   bigint not null,
    request_time    datetime not null,
    request_status  varchar(10) not null,
    request_action  varchar(10) not null,
    description     varchar(400) not null,

    primary key(id),
    foreign key(shopper_id) references account(id),
    foreign key(pantry_id) references pantry(id),
    check(request_status='pending'
        or request_status='approved'
        or request_status='denied'
    ),
    check(request_action='receive'
        or request_action='donate'
    )
);
create table inventory_item(
    id          bigint not null,
    generic_id  bigint not null,
    quantity    int not null,
    origin_id   bigint not null,
    expiration_date date,
    description     varchar(200),
    image           bytea,

    primary key(id),
    foreign key(generic_id) references generic_item(id),
    check(quantity>=0),
    foreign key(origin_id) references transaction(id)
);