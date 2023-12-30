const block_template = (index, type, message) => {
    return ` 
<div class="row">
    <div class="col-auto pt-2 d-flex flex-column">
        <div class="btn-group-vertical mb-2" role="group">
            <div id="up-btn-${index}" class="btn btn-outline-primary"><i class="bi bi-chevron-up"></i></div>
            <div id="down-btn-${index}" class="btn btn-outline-primary"><i class="bi bi-chevron-down"></i></div>
        </div>
        <div type="button" id="delete-block-btn-${index}" class="btn btn-danger"><i class="bi bi-x"></i></div>
    </div>
    <div class="col pt-2">
        <div class="mb-3">
            <label class="mb-1" for="type-select-${index}">Type: </label>
            <select name="" id="type-select-${index}" class="form-select">
                <option value="1" ${type == 1 ? "selected" : ""}>Text</option>
                <option value="2" ${type == 2 ? "selected" : ""}>Number</option>
            </select>
        </div>
        <div class="form-floating mb-3">
            <textarea name="" id="text-data-${index}" placeholder="Your message" class="form-control">${message}</textarea>
            <label for="text-data-${index}">Your message</label>
        </div>
    </div>
</div>
    `;
};

class QuestionModel {
    index;
    type = "1";
    message = "";
    hooked = false;

    // Listeners:
    type_input;
    message_input;
    delete_btn;
    up_btn;
    down_btn;

    // Handlers
    on_delete;
    on_up;
    on_down;
    on_message_changed;
    on_type_changed;

    constructor(index, on_delete, on_up, on_down) {
        this.index = index; 
        this.on_delete = on_delete;
        this.on_up = on_up;
        this.on_down = on_down;
        this.on_message_changed = (e) => this.message_changed(e, this);
        this.on_type_changed = (e) => this.type_changed(e, this);
    }

    hook_on_DOM() {
        this.hooked = true;

        this.type_input = document.getElementById(`type-select-${this.index}`);
        this.message_input = document.getElementById(`text-data-${this.index}`);

        this.delete_btn = document.getElementById(`delete-block-btn-${this.index}`);
        this.up_btn = document.getElementById(`up-btn-${this.index}`);
        this.down_btn = document.getElementById(`down-btn-${this.index}`);

        this.type_input.addEventListener("change", 
            this.on_type_changed);
        this.message_input.addEventListener("change", 
            this.on_message_changed);

        this.delete_btn.addEventListener("click", this.on_delete);
        this.up_btn.addEventListener("click", this.on_up);
        this.down_btn.addEventListener("click", this.on_down);
    }

    hook_off_DOM() {
        this.hooked = false;

        //Usually removing hooks is redundant but I was told there is memory leakage in firefox 
        this.type_input.removeEventListener("change", 
            this.on_type_changed);
        this.message_input.removeEventListener("change", 
            this.on_message_changed);

        this.delete_btn.removeEventListener("click", this.on_delete);
        this.up_btn.removeEventListener("click", this.on_up);
        this.down_btn.removeEventListener("click", this.on_down);
    }

    message_changed(event, context) {
        context.message = event.target.value;
    }

    type_changed(event, context) {
        context.type = event.target.value;
    }

    get_template() {
        return block_template(this.index, this.type, this.message);
    }
}

const questions = [];
const users = [
    {
        id: 1,
        name: "Bob"
    },
    {
        id: 2,
        name: "Tom"
    }
];

const insert_question_to_DOM = (question) => {
    document.getElementById('new-template').insertAdjacentHTML(
        'beforeend', question.get_template());
}

const redraw_questions = (questions) => {
    const base = document.getElementById('new-template');
    questions.forEach((element) => element.hooked && element.hook_off_DOM());

    base.replaceChildren();

    questions.forEach((element) => {
        insert_question_to_DOM(element);
        element.on_up = on_up_fabric(questions, element.index);
        element.on_down = on_down_fabric(questions, element.index);
        element.on_delete = on_delete_fabric(questions, element.index);
        element.hook_on_DOM();
    });
}

const on_delete_fabric = (questions, index) => {
   return () => {
       const pos = questions.findIndex(q => q.index === index);
       console.log(pos);
       questions[pos]?.hook_off_DOM();
       questions.splice(pos, 1);
       redraw_questions(questions);
   };
};

const on_up_fabric = (questions, index) => {
    return () => {
        const pos = questions.findIndex(q => q.index === index);
        if(pos === 0) return;

        const prev = questions[pos - 1];
        questions[pos].index = prev.index; prev.index = index;  
        questions.sort((q1, q2) => q1.index - q2.index);

        redraw_questions(questions);
    };
};

const on_down_fabric = (questions, index) => {
    return () => {
        const pos = questions.findIndex(q => q.index === index);
        console.log(pos);
        if(pos === questions.length - 1) return;

        const prev = questions[pos + 1];
        questions[pos].index = prev.index; prev.index = index;  
        questions.sort((q1, q2) => q1.index - q2.index);

        redraw_questions(questions);
    };
};


const add_new_question = (questions) => {
    const last_index = questions[questions?.length - 1]?.index ?? -1;
    const new_index = last_index + 1; 
    const new_question = new QuestionModel(
        new_index, 
        on_delete_fabric(questions, new_index),
        on_up_fabric(questions, new_index),
        on_down_fabric(questions, new_index)
    );

    questions.push(new_question);
    redraw_questions(questions);
};

document.getElementById('new-block-btn').addEventListener(
    "click", (e) => {add_new_question(questions);}
);
