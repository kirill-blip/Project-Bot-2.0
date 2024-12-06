CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL);
                       
       
CREATE TABLE IF NOT EXISTS admin(id SERIAL PRIMARY KEY,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                password TEXT NOT NULL,
                                table_number INTEGER NOT NULL);
       
       
CREATE TABLE IF NOT EXISTS entry(id SERIAL PRIMARY KEY,
                                ticket_number INTEGER NOT NULL,
                                user_id INTEGER NOT NULL,
                                admin_id INTEGER,
                                date TEXT NOT NULL,
                                status TEXT NOT NULL,
                                FOREIGN KEY (user_id)
                                    REFERENCES "user" (id));

CREATE OR REPLACE FUNCTION get_last_number(in_date TIMESTAMP)
RETURNS INT
AS $$
DECLARE 
    result INT;
BEGIN 
    SELECT MAX(ticket_number)
    INTO result
    FROM entry
    WHERE date = in_date;

    RETURN result;
END; 
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION notify_value_change()
RETURNS TRIGGER AS $$
DECLARE
    entry_id INTEGER;
BEGIN
    entry_id := NEW.id;
    raise notice 'Change';
    PERFORM pg_notify('value_change', '' || entry_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER value_change_trigger
AFTER UPDATE ON entry
FOR EACH ROW
EXECUTE FUNCTION notify_value_change();

CREATE OR REPLACE PROCEDURE save_entry(
    p_chat_id BIGINT,
    p_first_name TEXT,
    p_last_name TEXT,
    p_phone TEXT,
    p_ticket_number INT)
LANGUAGE plpgsql
AS $$
DECLARE
    user_id INT;
BEGIN
    INSERT INTO "user" (chat_id, first_name, last_name, phone)
    VALUES (p_chat_id, p_first_name, p_last_name, p_phone);

    user_id := (SELECT id FROM "user" WHERE chat_id = p_chat_id);


    INSERT INTO entry (ticket_number, user_id, date, status)
    VALUES (p_ticket_number, user_id, '2024/01/01', 'Waiting');    
END;
$$;

CREATE OR REPLACE PROCEDURE add_entry(i_chat_id bigint,
									  i_first_name text,
									  i_last_name text,
									  i_phone text,
									  i_ticket_number int,
									  i_date timestamp)
AS $$
DECLARE
	user_id INT;
BEGIN
	INSERT INTO "user" (chat_id, first_name, last_name, phone)
    VALUES (i_chat_id, i_first_name, i_last_name, i_phone);
	
	user_id := (SELECT id FROM "user" WHERE chat_id = i_chat_id);

	INSERT INTO entry (user_id, date, ticket_number, status)
    VALUES (user_id, i_date, i_ticket_number, 'Waiting'); 
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION check_status(t_chat_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    result TEXT;
BEGIN
    SELECT status 
    INTO result
    FROM entry 
    WHERE user_id = (SELECT id FROM "user" WHERE chat_id = t_chat_id );

    IF result = 'Waiting' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION has_entry_by_chat_id(t_chat_id BIGINT)
RETURNS BOOLEAN AS $$
DECLARE
    result RECORD;
BEGIN
    SELECT * 
    INTO result
    FROM entry 
    WHERE user_id = (SELECT id FROM "user" WHERE chat_id = t_chat_id );

    IF result IS NULL THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;
	
CREATE OR REPLACE PROCEDURE add_entry(
    p_chat_id BIGINT,
    p_first_name TEXT,
    p_last_name TEXT,
    p_phone TEXT,
    p_ticket_number INT,
    p_date TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INT;
    v_date DATE;
BEGIN
    v_date := TO_DATE(p_date, 'YYYY/MM/DD');

    INSERT INTO "user" (chat_id, first_name, last_name, phone)
    VALUES (p_chat_id, p_first_name, p_last_name, p_phone);

    SELECT id INTO v_user_id FROM "user" WHERE chat_id = p_chat_id;
    
    INSERT INTO entry (ticket_number, user_id, date, status)
    VALUES (p_ticket_number, v_user_id, v_date, 'Waiting');
END;
$$;

CREATE OR REPLACE PROCEDURE add_user(i_chat_id bigint,
									  i_first_name text,
									  i_last_name text,
									  i_phone text)
AS $$
DECLARE
	user_id INT;
BEGIN
	INSERT INTO "user" (chat_id, first_name, last_name, phone)
    VALUES (i_chat_id, i_first_name, i_last_name, i_phone); 
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE add_entry(i_chat_id bigint,
									  i_ticket_number int,
									  i_date timestamp)
AS $$
DECLARE
	user_id INT;
BEGIN
	user_id := (SELECT id FROM "user" WHERE chat_id = i_chat_id);

	INSERT INTO entry (user_id, date, ticket_number, status)
    VALUES (user_id, i_date, i_ticket_number, 'Waiting'); 
END; $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION has_user(t_chat_id BIGINT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (SELECT 1 FROM "user" WHERE "user".chat_id = t_chat_id);
END;
$$ LANGUAGE plpgsql;

create or replace procedure update_user(i_chat_id bigint,
									  i_first_name text,
									  i_last_name text,
									  i_phone text)
as $$
begin 
	update "user" 
	set first_name = i_first_name,
		last_name = i_last_name,
		phone = i_phone
	where chat_id = i_chat_id;
end; $$ language plpgsql;
