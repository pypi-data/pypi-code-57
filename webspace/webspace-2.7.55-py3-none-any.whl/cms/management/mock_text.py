import random
from django.utils import lorem_ipsum


def title():
    return lorem_ipsum.words(random.randint(5, 15))


def text(rand_min=100, rand_max=200):
    return lorem_ipsum.words(random.randint(rand_min, rand_max))


class MockText(object):
    h = f"""
    {title()}
    """

    xs = f"""
        <h3>{title()}</h3>
        <p>{text(10, 10)}</p>
        """

    small = f"""
        <h2>{title()}</h2>
        <h3>{title()}</h3>
        <hr/>
        <p>{text(20, 20)}</p>
        """

    normal = f"""
    <h3>{title()}</h3>
    <hr/>
    <p>{text(50, 50)}</p>
    """

    big = f"""
    <h2>{title()}</h2>
    <h3>{title()}</h3>
    <h4>{title()}</h4>
    <hr/>
    <p>{title()}</p>
    <ol>
        <li>{title()}</li>
        <li>{title()}</li>
        <li>{title()}</li>
        <li>{title()}</li>
    </ol>
    <p>{title()}</p>
    <p><b>{title()}</b><i>{title()}</i></p>
    <p><i>{title()}</i></p>
    <ul>
        <li>{title()}</li>
        <li>{title()}</li>
        <li>{title()}</li>
        <li>{title()}</li>
    </ul>
    <p></p>
    <p></p>
    <p>{text()}</p>
    <p><a href="#">{title()}</a>. {text()}</p><p><br/></p>
    """

    example = f"""
    <h1>H1 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h1>
    <h2>H2 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
    <h3>H3 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h3>
    <h4>H4 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h4>
    <h5>H5 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h5>
    <h6>H6 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h6>
    <hr/>
    <p>Paragraph -> {title()}</p>
    <p><b>Bold -> {title()}</b></p>
    <p><i>Italic -> {title()}</i></p>
    <p><strong>Strong -> {title()}</strong></p>
    """

    text_first_content = f"""
    <h2>Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
    <hr/>
    <p>{title()}</p>
    """

    form = f"""
    <section class="padding">
        <form action="#" autocomplete="off">
            <div class="form-group">
                <label>Email</label>
                <div class="input-img">
                    <img src="/static/assets/img/svg/icons/rocket/space.svg">
                    <input name="email" type="email" placeholder="Email" autocomplete="off" value="">
                </div>
                <small>We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
                <label>Password</label>
                <div class="input-img">
                    <img src="/static/assets/img/svg/icons/rocket/space.svg">
                    <input name="password" type="password" placeholder="Password" autocomplete="off" value="">
                </div>
                <small>Limit of 10 caracters</small>
            </div>
            <div class="form-group">
                <label>Name</label>
                <div class="input-img">
                    <img src="/static/assets/img/svg/icons/rocket/space.svg">
                    <input name="name" type="text" placeholder="Name" autocomplete="off" value="">
                </div>
                <small>Limit of 10 caracters</small>
            </div>
            <div class="form-group error">
                <label>Name</label>
                <div class="input-img">
                    <img src="/static/assets/img/svg/icons/rocket/space.svg">
                    <input name="name" type="text" placeholder="Name" autocomplete="off" value="">
                </div>
                <small>Limit of 10 caracters</small>
            </div>
            <div class="form-group">
                <label>Textarea</label>
                <textarea  rows="3"></textarea>
                <small>Info</small>
            </div>
            <div class="form-group">
                <label>Checkbox On</label>
                <div class="checkbox-container">
                    <input type="checkbox" class="checkbox" checked="checked">
                    <div class="knobs"></div>
                    <div class="layer"></div>
                </div>
            </div>
            <div class="form-group">
                <label>Checkbox Off</label>
                <div class="checkbox-container">
                    <input type="checkbox" class="checkbox">
                    <div class="knobs"></div>
                    <div class="layer"></div>
                </div>
            </div>
            <div class="form-group">
                <label>Example select</label>
                <select>
                  <option>Choice 1</option>
                  <option>Choice 2</option>
                  <option>Choice 3</option>
                  <option>Choice 4</option>
                  <option>Choice 5</option>
                </select>
                <small>Info</small>
            </div>
            <div class="form-group">
                <label>Radio</label>
                <div class="form-check">
                  <input type="radio" name="radio" checked>
                  <label>Radio 1</label>
                </div>
                <div class="form-check">
                  <input type="radio" name="radio">
                  <label>Radio 2</label>
                </div>
                <div class="form-check">
                  <input type="radio" name="radio">
                  <label>Radio 3</label>
                </div>
            </div>
            <fieldset>
                <legend>Legend</legend>
                <div class="form-group">
                    <label>Email</label>
                    <div class="input-img">
                        <img src="/static/assets/img/svg/icons/rocket/space.svg">
                        <input name="email" type="email" placeholder="Email" autocomplete="off" value="">
                    </div>
                    <small>We'll never share your email with anyone else.</small>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <div class="input-img">
                        <img src="/static/assets/img/svg/icons/rocket/space.svg">
                        <input name="password" type="password" placeholder="Password" autocomplete="off" value="">
                    </div>
                    <small>Limit of 10 caracters</small>
                </div>
            </fieldset>
            <div class="form-group">
                <label>Range</label>
                <input name="range" type="range" min="100" max="400">
                <small>100 to 400</small>
            </div>
        </form>
    </section>
    """
